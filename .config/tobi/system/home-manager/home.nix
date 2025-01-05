{ lib, pkgs, ... }:
{
  home = {
    packages = with pkgs; [
      hello
      cowsay
      lolcat
    ];

    # This needs to actually be set to your username
    username = "tobi";
    homeDirectory = "/home/tobi";

    # You do not need to change this if you're reading this in the future.
    # Don't ever change this after the first build.  Don't ask questions.
    stateVersion = "23.11";
  };
}
