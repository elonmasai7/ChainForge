module creatorchain::revenue_router {
    use std::signer;

    struct CreatorVault has key {
        owner: address,
        balance: u64,
    }

    public entry fun init_vault(account: &signer) {
        move_to(account, CreatorVault { owner: signer::address_of(account), balance: 0 });
    }

    public entry fun credit_vault(account: &signer, amount: u64) {
        let vault = borrow_global_mut<CreatorVault>(signer::address_of(account));
        vault.balance = vault.balance + amount;
    }
}
