from decimal import Decimal
from django.db.models import Sum
from .models import Bet, Event

# The standard house cut is 10%
HOUSE_CUT_PERCENTAGE = Decimal('0.10')

def calculate_event_stats(event):
    """
    Calculates all financial stats for a given event
    """
    
    # Get the sum of bets for each choice
    meron_total = Bet.objects.filter(event=event, bet_choice='Meron').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    wala_total = Bet.objects.filter(event=event, bet_choice='Wala').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Calculate the pools
    total_wager = meron_total + wala_total
    house_cut = total_wager * HOUSE_CUT_PERCENTAGE
    net_pool = total_wager - house_cut
    
    # Calculate odds and total payout for each side
    meron_odds = net_pool / meron_total if meron_total > 0 else Decimal('0.00')
    wala_odds = net_pool / wala_total if wala_total > 0 else Decimal('0.00')
    
    meron_payout = meron_total * meron_odds
    wala_payout = wala_total * wala_odds
    
    return {
        'total_wager': total_wager,
        'house_cut': house_cut,
        'net_pool': net_pool,
        'meron_total_wager': meron_total,
        'wala_total_wager': wala_total,
        'meron_odds': round(meron_odds, 4),
        'wala_odds': round(wala_odds, 4),
        'meron_total_payout': meron_payout,
        'wala_total_payout': wala_payout,
    }
    
    
def calculate_financial_summary():
    """
    Calculates the financial summary across all operations.
    """
    # Get the sum of all bets from events that are closed for betting.
    total_wagers = Bet.objects.filter(event__is_closed=True).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Get the sum of all payouts that have been marked as WON.
    total_payouts = Bet.objects.filter(payout_status='WON').aggregate(total=Sum('payout_amount'))['total'] or Decimal('0.00')

    # The house cut (rake) is the difference.
    total_rake = total_wagers - total_payouts

    return {
        'total_wagers': total_wagers,
        'total_payouts': total_payouts,
        'total_rake': total_rake,
        'completed_matches': Event.objects.filter(is_closed=True).count()
    }

def process_event_payouts(event, winner):
    """
    Finalizes an event, calculates payouts, and updates all bets.
    This is the core function for closing a fight.
    """
    if event.is_closed:
        # Prevent processing the same event twice
        raise ValueError("This event has already been closed.")

    # 1. Close the event and declare the winner
    event.is_closed = True
    event.is_active = False
    event.outcome = winner
    event.save()

    # 2. Get the final financial stats and payout ratios
    final_stats = calculate_event_stats(event)
    meron_payout_ratio = final_stats.get('meron_odds', Decimal('0.00'))
    wala_payout_ratio = final_stats.get('wala_odds', Decimal('0.00'))

    # 3. Get all bets for this event
    bets_to_update = Bet.objects.filter(event=event)

    # 4. Loop through every bet and update its status and payout amount
    for bet in bets_to_update:
        is_winner = (bet.bet_choice.upper() == winner.upper())

        if is_winner:
            bet.payout_status = 'WON'
            if winner.upper() == 'MERON':
                bet.payout_amount = bet.amount * meron_payout_ratio
            else: # Winner is WALA
                bet.payout_amount = bet.amount * wala_payout_ratio
        else:
            bet.payout_status = 'LOST'
            bet.payout_amount = Decimal('0.00')

        bet.save()

    return {"status": "success", "message": f"Event finalized. Winner: {winner}"}