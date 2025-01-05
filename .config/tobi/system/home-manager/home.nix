{ lib, pkgs, ... }:
{
  home = {
    packages = with pkgs; [

      # basic functionality
      neovim       # best editor
      alacritty    # terminal
      xclip        # put something into clipboard
      fzf          # fuzzy find
      killall
      unzip        # uncompress files
      tmux         # yea terminal stuff
      zoxide       # nicer cd
      bat          # cat with colors
      eza          # like ls
      ripgrep      # searching files by text
      jq           # json parsing
      dunst        # displaying desktop notifications
      libnotify    # sending desktop notifications
      keepassxc    # passwords

      pywal        # set the wallpaper and color scheme
      picom        # window transparency and stuff

      git          # version control
      gh           # git interacting with github

      gnumake      # for building dependencies
      gcc          # compiler

      nodejs       # frontend development

      xdotool      # get the title of a window
      wmctrl       # rename active window
      rofi         # window switcher

    ];

    # This needs to actually be set to your username
    username = "tobi";
    homeDirectory = "/home/tobi";

    # You do not need to change this if you're reading this in the future.
    # Don't ever change this after the first build.  Don't ask questions.
    stateVersion = "23.11";
  };
}
