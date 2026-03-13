"use client";

import { PropsWithChildren } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WagmiProvider, createConfig, http } from "wagmi";
import { mainnet } from "wagmi/chains";
import {
  PrivyProvider,
  useCreateWallet,
  useLoginWithSiwe,
  usePrivy,
  useWallets,
} from "@privy-io/react-auth";
import { InterwovenKitProvider } from "@initia/interwovenkit-react";

const queryClient = new QueryClient();

const wagmiConfig = createConfig({
  chains: [mainnet],
  transports: {
    [mainnet.id]: http(),
  },
});

function InterwovenKitWrapper({ children }: PropsWithChildren) {
  const privy = usePrivy();
  const siwe = useLoginWithSiwe();
  const { createWallet } = useCreateWallet();
  const { wallets } = useWallets();

  return (
    <InterwovenKitProvider
      privyContext={{
        privy,
        siwe,
        createWallet,
        wallets,
      }}
      enableAutoSign
      autoSignConfig={{
        chains: [
          {
            chainId: process.env.NEXT_PUBLIC_INITIA_CHAIN_ID || "creatorchain-1",
            messages: ["/cosmos.bank.v1beta1.MsgSend", "/initia.move.v1.MsgExecute"],
          },
        ],
      }}
    >
      {children}
    </InterwovenKitProvider>
  );
}

export function Providers({ children }: PropsWithChildren) {
  return (
    <QueryClientProvider client={queryClient}>
      <WagmiProvider config={wagmiConfig}>
        <PrivyProvider
          appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID || ""}
          config={{
            embeddedWallets: {
              ethereum: {
                createOnLogin: "all-users",
              },
            },
            loginMethodsAndOrder: {
              primary: ["google", "twitter"],
            },
          }}
        >
          <InterwovenKitWrapper>{children}</InterwovenKitWrapper>
        </PrivyProvider>
      </WagmiProvider>
    </QueryClientProvider>
  );
}
