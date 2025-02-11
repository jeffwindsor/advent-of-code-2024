{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	
    # name (default: nix-shell). Set the name of the derivation.
	# name = "";
  	
    # packages (default: []). Add executable packages to the nix-shell environment.
	packages = with pkgs; [
    (python312.withPackages(p: with p; [
        python-lsp-server
        # ruff
        # mypy
        black
        pytest
      ]))
	];

    # inputsFrom (default: []). Add build dependencies of the listed derivations to the nix-shell environment.
	# inputsFrom = [ pkgs.hello ];

    # shellHook (default: ""). Bash statements that are executed by nix-shell.
  	shellHook = ''
    	echo -e "\e[1;33mDevelopment Environment\e[0;32m"
      python --version
      pylsp --version
      pytest --version
      echo -e "\e[0m"
  	'';
}
