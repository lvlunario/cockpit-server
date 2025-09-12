from decimal import Decimal
from django.db.models import Sum
from .models import Bet

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