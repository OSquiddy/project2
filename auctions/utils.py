from .models import User, Listing, Bid, Comment, WatchList
from django.http import JsonResponse
from django.forms.models import model_to_dict  

def makeWatchList(user, listing):
    try:
        watchlist = WatchList.objects.get(user=user)
    except WatchList.DoesNotExist:
        watchlist = WatchList.objects.create_watchlist(user)
        watchlist.save()
    watchlist.listings.add(listing)
    
def removeFromWatchList(user, listing):
    try:
        watchlist = WatchList.objects.get(user=user)

        watchlist.listings.remove(listing)
        watchlist.save()
    except WatchList.DoesNotExist:
        pass

def makeBid(user, listing, bidPrice):
    try:
        bid = Bid.objects.get(user=user, listing=listing)
    except Bid.DoesNotExist:
        bid = Bid(user=user, listing=listing)
    bid.price = bidPrice
    bid.save()

def setBidWinner(listing):
    bids = Bid.objects.filter(listing = listing)
    top = 0
    for bid in bids:
        if bid.price > top:
            top = bid.price
    bid = Bid.objects.get(price=top)
    bid.winning_Bid = True
    bid.save()

def clearBidWinner(listing):
    bids = Bid.objects.filter(listing = listing)
    for bid in bids:
        bid.winning_Bid = False
        bid.save()

def getCommentList(listing):
    # commentList = Comment.objects.filter(listing=listing).order_by('-datetime')
    commentList = Comment.objects.filter(listing=listing)
    return commentList
    
def addComment(listing, user, comment):
    comment = Comment(user=user, listing=listing, comment=comment)
    comment.save()

def getLatestBid(listing):
    bid = Bid.objects.filter(listing=listing).order_by('-datetime').first()
    return bid

def getRecentViewsList(request, listing):
    try:
        if listing.id in request.session['history']:
            print("It was in history")
            request.session['history'].remove(listing.id)
            request.session.setdefault('history', []).append(listing.id)
        else:
            print("It wasn't in history")
            request.session.setdefault('history', []).append(listing.id)
        request.session.modified = True
    except KeyError:
        request.session.setdefault('history', []).append(listing.id)
        request.session.modified = True
    data = request.session.get('history')
    finalList = list(data)
    print("Length of finalList is ", len(finalList))
    if len(finalList) > 5:
        del finalList[0]
        print(len(finalList))
    return finalList[-6:-1]

def getOtherItemsBySeller(listing):
    otherItemsList = Listing.objects.filter(user=listing.user).exclude(id=listing.id)
    if len(otherItemsList) > 5:
        return otherItemsList[:5]
    else:
        return otherItemsList
    
def getOtherSellers(listing):
    otherSellersList = User.objects.filter(listings__isnull=False).distinct().exclude(id=listing.user_id)
    print(otherSellersList)
    return otherSellersList

def getCategoryPosters():
    postertuple = (
        ("el" , "https://i.pinimg.com/564x/85/7a/08/857a0822efcb34fe949b6b822b346b53.jpg"),
        ("sp" , "https://i.pinimg.com/564x/2c/9b/95/2c9b953aad8774054ddb6cd2525230be.jpg"),
        ("ed" , "https://i.pinimg.com/564x/cc/05/0b/cc050b7fe9b25c16836627df149a6b92.jpg"),
        # ("ty" , "https://i.pinimg.com/564x/f2/e3/22/f2e3220be28f99a46a4d4e87032d6c06.jpg"),
        ("ty" , "https://i.pinimg.com/564x/f1/26/25/f12625f6861f14be64773b59d3a1f23a.jpg"),
        ("bk" , "https://i.pinimg.com/564x/a1/22/19/a12219b4f8dcecac3611e5385efcd340.jpg"),
        ("ar" , "https://i.pinimg.com/564x/de/c1/17/dec117acdcd03eaceb64d7493856f5a5.jpg"),
        ("lx" , "https://i.pinimg.com/564x/73/1a/eb/731aeb9f7887cab9a7db1cc2d5d40738.jpg"),
        ("cl" , "https://i.pinimg.com/564x/81/31/15/8131152feef686a36aa278047e4e3d14.jpg"),
        ("jw" , "https://i.pinimg.com/564x/b6/56/bd/b656bd30ad05c5efcd2955a0183d6643.jpg"),
        ("bf" , "https://i.pinimg.com/564x/0e/fb/e8/0efbe8dbb469b55a1b5768b6b93ed7b9.jpg"),
        ("hm" , "https://cdn.flbx.io/aHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbS9wL0I5SGpMQlRodzUwLw==/thumbnail_512"),
        ("ac" , "https://i.pinimg.com/236x/ca/b0/7d/cab07d006fcb3b7009d1ef12bb9c4625.jpg")
    )
    return postertuple
    