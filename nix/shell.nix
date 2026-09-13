{
  perSystem = {
    pkgs,
    lib,
    config,
    ...
  }: {
    options.shellPackages = lib.mkOption {
      type = lib.types.listOf lib.types.package;
      default = [];
    };
    config.devShells.default = pkgs.mkShell {
      name = "project-dev-env";
      packages = lib.unique config.shellPackages;

      # Every tool comes from nix. Stop moon from injecting proto shims
      # and proto toolchains into the task PATH.
      MOON_TOOLCHAIN_FORCE_GLOBALS = "1";
    };
  };
}
