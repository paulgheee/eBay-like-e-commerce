# Commerce - Ebay Clone

#### Youtube Video Demo: <[URL HERE](https://www.youtube.com/watch?v=x6XXZku2PZE)>

### Description
An eBay-like e-commerce auction site that allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”
- **```Models:```** User, AuctionListings, Comments, Bids
- **```Create Listing:```** Users are able to visit a page to create a new listing. They are able to specify a title for the listing, a text-based description, and what the starting bid should be. Users are also optionally able to provide a URL for an image for the listing and/or a category.
- **```Active Listings Page:```** The default route of the web application let users view all of the currently active auction listings. For each active listing, this page dysplay the title, description, current price, and photo.
- **```Listing Page:```** Clicking on a listing take users to a page specific to that listing. On that page, users are able to view all details about the listing:
    -  If the user is signed in, the user are able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). 
    - If the user is signed in and is the one who created the listing, the user have the ability to "close" the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    - If a user is signed in on a closed listing page, and the user has won that auction, the page whould say so.
    - Users who are signed in are able to add comments to the listing page. The listing page will display all coments that have been made on the listing.
- **```Watchlist:```** Users who are signed in are able to visit a Watchlist page, which display all of the listings that a user has added to their watchlist. Each listing will show if it is active or close. Clicking on any of those listings will take the user to that listing`s page.
- **```Categories:```** Users are able to visit a page that displays a list of all listing categories. Clicking on the name of any category wil take the user to a page that displays all of the active listings in that category.