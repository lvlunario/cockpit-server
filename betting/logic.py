from decimal import Decimal
from django.db.models import Sum, Count
from .models import Bet, Event

SIDE_COMMISSION_PERCENTAGE = Decimal('0.05')

def calculate_event_stats(event):
    """
    Calculates all financial stats for a given event based on the new commission rule.
    """
    meron_entries = Bet.objects.filter(event=event, bet_choice='Meron')
    wala_entries = Bet.objects.filter(event=event, bet_choice='Wala')
    draw_entries = Bet.objects.filter(event=event, bet_choice='Draw')

    meron_total = meron_entries.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    wala_total = wala_entries.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    draw_total = draw_entries.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Calculate the commission from each side
    meron_commission = meron_total * SIDE_COMMISSION_PERCENTAGE
    wala_commission = wala_total * SIDE_COMMISSION_PERCENTAGE
    
    # The total system cut is the sum of commissions from both main sides
    system_cut = meron_commission + wala_commission

    # The net pool is what's left for payouts
    total_meron_wala_points = meron_total + wala_total
    net_pool = total_meron_wala_points - system_cut

    # Calculate payout ratios based on the net pool
    meron_ratio = net_pool / meron_total if meron_total > 0 else Decimal('0.00')
    wala_ratio = net_pool / wala_total if wala_total > 0 else Decimal('0.00')

    return {
        'total_points': meron_total + wala_total + draw_total,
        'system_cut': system_cut,
        'net_pool': net_pool,
        'meron_total_points': meron_total,
        'wala_total_points': wala_total,
        'draw_total_points': draw_total,
        'meron_entry_count': meron_entries.count(),
        'wala_entry_count': wala_entries.count(),
        'draw_entry_count': draw_entries.count(),
        'meron_payout_ratio': round(meron_ratio, 4),
        'wala_payout_ratio': round(wala_ratio, 4),
        'meron_total_payout': meron_total * meron_ratio,
        'wala_total_payout': wala_total * wala_ratio,
        'betting_status': event.betting_status,
        'outcome': event.outcome,
    }

def process_event_payouts(event, winner):
    """
    Finalizes an event, calculates payouts, and updates all entries.
    """
    if event.is_closed:
        raise ValueError("This event has already been closed.")

    event.is_closed = True
    event.is_active = None
    event.outcome = winner
    event.betting_status = 'CLOSED' # Update status on finish
    event.save()

    entries_to_update = Bet.objects.filter(event=event)
    final_stats = calculate_event_stats(event)

    if winner.upper() == 'DRAW':
        # For a draw, the system takes its commission from all entries, and the rest is refunded.
        for entry in entries_to_update:
            entry.payout_status = 'REFUNDED'
            entry.payout_amount = entry.amount * (Decimal('1.00') - SIDE_COMMISSION_PERCENTAGE)
            entry.save()
    else: # Meron or Wala wins
        meron_payout_ratio = final_stats.get('meron_payout_ratio', Decimal('0.00'))
        wala_payout_ratio = final_stats.get('wala_payout_ratio', Decimal('0.00'))
        for entry in entries_to_update:
            if entry.bet_choice.upper() == winner.upper():
                entry.payout_status = 'WON'
                if winner.upper() == 'MERON':
                    entry.payout_amount = entry.amount * meron_payout_ratio
                else: # Winner is WALA
                    entry.payout_amount = entry.amount * wala_payout_ratio
            else:
                entry.payout_status = 'LOST'
                entry.payout_amount = Decimal('0.00')
            entry.save()
    return {"status": "success", "message": f"Event finalized. Outcome: {winner}"}

def calculate_financial_summary():
    # This function remains unchanged but is included for completeness
    total_points = Bet.objects.filter(event__is_closed=True).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_payouts = Bet.objects.filter(payout_status__in=['WON', 'REFUNDED']).aggregate(total=Sum('payout_amount'))['total'] or Decimal('0.00')
    total_rake = total_points - total_payouts
    return {'total_wagers': total_points, 'total_payouts': total_payouts, 'total_rake': total_rake}

