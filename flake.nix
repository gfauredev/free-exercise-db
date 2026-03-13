{
  description = "Nix-flake web development environment";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs =
    { self, nixpkgs }:
    let
      systems =
        f:
        nixpkgs.lib.genAttrs [
          "x86_64-linux" # "aarch64-linux"
          # "aarch64-darwin"
        ] (system: f { pkgs = import nixpkgs { inherit system; }; });
    in
    {
      devShells = systems (
        { pkgs }:
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              # biome
              # bun # Faster runtime, bundler, package manager
              cmake
              cmake-format
              cmake-language-server
              cmake-lint
              check-jsonschema
              taplo # TOML LSP
              # typescript
              # typescript-language-server # TS LSP
              vscode-langservers-extracted # HTML/CSS/JS(ON)
              yaml-language-server # YAML LSP
              # deno # More secure runtime
              # node2nix
              # nodejs
              # nodePackages.pnpm
              # yarn
            ];
          };
        }
      );
    };
}
