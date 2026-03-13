module creatorchain::creator_registry {
    use std::signer;
    use std::string::String;
    use std::vector;

    struct Creator has store, drop {
        id: u64,
        name: String,
        handle: String,
        wallet: address,
    }

    struct Platform has store, drop {
        id: u64,
        creator_id: u64,
        name: String,
        monetization_type: String,
        pricing_model: String,
    }

    struct Registry has key {
        creators: vector<Creator>,
        platforms: vector<Platform>,
        next_creator_id: u64,
        next_platform_id: u64,
    }

    public entry fun init_registry(account: &signer) {
        move_to(account, Registry { creators: vector::empty<Creator>(), platforms: vector::empty<Platform>(), next_creator_id: 1, next_platform_id: 1 });
    }

    public entry fun register_creator(account: &signer, name: String, handle: String) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        let creator = Creator { id: registry.next_creator_id, name, handle, wallet: signer::address_of(account) };
        vector::push_back(&mut registry.creators, creator);
        registry.next_creator_id = registry.next_creator_id + 1;
    }

    public entry fun register_platform(account: &signer, creator_id: u64, name: String, monetization_type: String, pricing_model: String) {
        let registry = borrow_global_mut<Registry>(signer::address_of(account));
        let platform = Platform { id: registry.next_platform_id, creator_id, name, monetization_type, pricing_model };
        vector::push_back(&mut registry.platforms, platform);
        registry.next_platform_id = registry.next_platform_id + 1;
    }
}
