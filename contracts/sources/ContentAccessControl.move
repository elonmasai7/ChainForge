module creatorchain::content_access_control {
    use std::signer;
    use std::vector;

    struct AccessGrant has store, drop {
        content_id: u64,
        user: address,
    }

    struct Registry has key {
        grants: vector<AccessGrant>,
    }

    public entry fun init(account: &signer) {
        move_to(account, Registry { grants: vector::empty<AccessGrant>() });
    }

    public entry fun grant_access(account: &signer, content_id: u64, user: address) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        vector::push_back(&mut registry.grants, AccessGrant { content_id, user });
    }
}
