module creatorchain::marketplace_engine {
    use std::signer;
    use std::vector;

    struct Listing has store, drop {
        id: u64,
        creator: address,
        title: vector<u8>,
        price_amount: u64,
    }

    struct Registry has key {
        listings: vector<Listing>,
        next_id: u64,
    }

    public entry fun init(account: &signer) {
        move_to(account, Registry { listings: vector::empty<Listing>(), next_id: 1 });
    }

    public entry fun list_item(account: &signer, title: vector<u8>, price_amount: u64) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        let listing = Listing { id: registry.next_id, creator: signer::address_of(account), title, price_amount };
        vector::push_back(&mut registry.listings, listing);
        registry.next_id = registry.next_id + 1;
    }
}
