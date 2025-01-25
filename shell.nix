{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	
    # name (default: nix-shell). Set the name of the derivation.
	name = "Advent of Code 2024";
  	
    # packages (default: []). Add executable packages to the nix-shell environment.
	packages = with pkgs; [
	    python312
	    python312Packages.pytest
	    python312Packages.numpy
	];

    # inputsFrom (default: []). Add build dependencies of the listed derivations to the nix-shell environment.
	# inputsFrom = [ pkgs.hello ];

    # shellHook (default: ""). Bash statements that are executed by nix-shell.
  	shellHook = ''
    	echo "Let the fun begin"
  	'';
}
