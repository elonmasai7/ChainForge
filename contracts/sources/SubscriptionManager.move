module creatorchain::subscription_manager {
    use std::signer;
    use std::vector;

    struct Subscription has store, drop {
        id: u64,
        platform_id: u64,
        user: address,
        price_amount: u64,
        price_denom: vector<u8>,
        active: bool,
    }

    struct Registry has key {
        subs: vector<Subscription>,
        next_id: u64,
    }

    public entry fun init(account: &signer) {
        move_to(account, Registry { subs: vector::empty<Subscription>(), next_id: 1 });
    }

    public entry fun subscribe(account: &signer, platform_id: u64, price_amount: u64, price_denom: vector<u8>) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        let sub = Subscription { id: registry.next_id, platform_id, user: signer::address_of(account), price_amount, price_denom, active: true };
        vector::push_back(&mut registry.subs, sub);
        registry.next_id = registry.next_id + 1;
    }

    public entry fun cancel(account: &signer, sub_id: u64) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        let mut i = 0;
        while (i < vector::length(&registry.subs)) {
            let sub_ref = &mut vector::borrow_mut(&mut registry.subs, i);
            if (sub_ref.id == sub_id && sub_ref.user == signer::address_of(account)) {
                sub_ref.active = false;
                return;
            };
            i = i + 1;
        };
    }
}
