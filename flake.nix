{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    { systems, nixpkgs, ... }@inputs:
    let
      eachSystem = f: nixpkgs.lib.genAttrs (import systems) (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = eachSystem (pkgs: {
        default = pkgs.mkShell {
          buildInputs = [
            pkgs.nodejs_22
            pkgs.nodePackages.typescript
            pkgs.nodePackages.typescript-language-server

            pkgs.python313
            pkgs.python3Packages.venvShellHook
          ];

          venvDir = "./.venv";

          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            make init
          '';

          postShellHook = ''
            SOURCE_DATE_EPOCH=$(date +%s)
            make install
          '';
        };
      });

      packages = eachSystem (pkgs: {
        default = pkgs.python313;
      });

      defaultPackage = eachSystem (pkgs: {
        default = pkgs.python313;
      });

      docker = eachSystem (pkgs: pkgs.dockerTools.buildLayeredImage {
        name = "cerberus";
        tag = "latest";
        contents = [
          pkgs.python313
        ];
        config = {
          Cmd = [ "python" ];
        };
      });
    };
}
