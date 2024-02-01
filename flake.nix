{
  outputs = { self, nixpkgs }: let
    forAllSystems = f: nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ] (system: f (
      import nixpkgs {
    	inherit system;
      }
    ));
  in {
    packages = forAllSystems (pkgs: {
    	default = pkgs.stdenv.mkDerivation rec {
    	  name = "hass-addons-scripts";
    	  propagatedBuildInputs = with pkgs.python3Packages; [ GitPython docker pyyaml requirements-parser pkgs.socat ];
    	  src = ./scripts/.;
    	  installPhase = ''
    	      install -Dm755 common.py $out/bin/common.py
    	      install -Dm755 build.py $out/bin/build.py
    	      install -Dm755 run.py $out/bin/run.py
    	      install -Dm755 publish.py $out/bin/publish.py
    	      install -Dm755 outdated.py $out/bin/outdated.py
    	  '';
    	};
    });
  
    devShells = forAllSystems (pkgs: {
      default = pkgs.mkShell {
      	packages = [ self.packages."${pkgs.system}".default ];
      	shellHook = ''
      	    alias build="build.py"
      	    alias run="run.py"
      	    alias publish="publish.py"
      	    alias outdated="outdated.py"
      	
      	    echo "Commands:"
            echo "build     [addon]             -   build a addon"
            echo "run       [addon]             -   run a addon"
            echo "publish   [addon] [version]   -   publish a addon"
            echo "outdated                      -   check for outdated packages"
        '';
      };
    });
  };
}
