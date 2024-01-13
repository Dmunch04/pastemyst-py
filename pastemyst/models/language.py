from enum import Enum
from typing import Dict, List, Any, Optional

from pastemyst.utils import camel_to_snake, mangle_attr


class LanguageInfo:
    """

    Represents information about a programming language used in pastemyst.

    Attributes:
        - name (str): The name of the language.
        - mode (str): The mode of the language used in the pastemyst editor.
        - mimes (List[str]): The list of MIME types used by the language.
        - extensions (Optional[List[str]]): The list of file extensions used by the language. Returns None if no extensions are available.
        - color (Optional[str]): The color of the language used in the pastemyst editor. Returns None if no color is set.

    Methods:
        - from_dict(data: Dict[str, Any]) -> LanguageInfo: Convert a dictionary into a LanguageInfo object.

    """
    __slots__ = ("__name", "__mode", "__mimes", "__ext", "__color")

    @property
    def name(self) -> str:
        """
        :return: The name of the language
        :rtype: str
        """
        return self.__name

    @property
    def mode(self) -> str:
        """
        Get the mode of the language.
        Used in the pastemyst editor

        :return: The mode of the language.
        :rtype: str
        """
        return self.__mode

    @property
    def mimes(self) -> List[str]:
        """
        Get the list of MIME types used by the language.

        :return: The list of MIME types used by the language.
        :rtype: List[str]
        """
        return self.__mimes

    @property
    def extensions(self) -> Optional[List[str]]:
        """
        Get the list of file extensions used by the language.

        :return: A list of file extensions or None if no extensions are available.
        :rtype: Optional[List[str]]
        """
        return self.__ext or None

    @property
    def color(self) -> Optional[str]:
        """
        Get the color of the language.
        Used in the pastemyst editor

        :return: The color of the language, if available. Returns None if no color is set.
        :rtype: Optional[str]
        """
        return self.__color or None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LanguageInfo":
        """
        Convert a dictionary into a LanguageInfo object.

        :param data: Dictionary containing the data to be converted.
        :type data: Dict[str, Any]
        :return: LanguageInfo object converted from the dictionary data.
        :rtype: LanguageInfo
        """
        language_info: LanguageInfo = LanguageInfo()
        for key, value in data.items():
            key = camel_to_snake(key)

            if key == "file":
                continue

            language_info.__setattr__(mangle_attr(language_info, f"__{key}"), value)

        return language_info


class Language(str, Enum):
    """
    This class represents a set of programming languages. Each language is defined as a string constant.

    Attributes:
        AUTODETECT (str): The Autodetect language.
        PLAIN (str): Plain Text language.
        APL (str): APL language.
        PGP (str): PGP language.
        ASN1 (str): ASN.1 language.
        ASTERISK (str): Asterisk language.
        BRAINFUCK (str): Brainfuck language.
        CLANG (str): C language.
        C (str): C language.
        CPP (str): C++ language.
        COBOL (str): Cobol language.
        CSHARP (str): C# language.
        CLOJURE (str): Clojure language.
        CLOJURE_SCRIPT (str): ClojureScript language.
        GSS (str): Closure Stylesheets (GSS) language.
        CMAKE (str): CMake language.
        COFFEE_SCRIPT (str): CoffeeScript language.
        LISP (str): Common Lisp language.
        CYPHER (str): Cypher language.
        CYTHON (str): Cython language.
        CRYSTAL (str): Crystal language.
        CSS (str): CSS language.
        CQL (str): CQL language.
        DLANG (str): D language.
        D (str): D language.
        DART (str): Dart language.
        DIFF (str): diff language.
        DJANGO (str): Django language.
        DOCKER (str): Dockerfile language.
        DTD (str): DTD language.
        DYLAN (str): Dylan language.
        EBNF (str): EBNF language.
        ECL (str): ECL language.
        EDN (str): edn language.
        EIFFEL (str): Eiffel language.
        ELM (str): Elm language.
        EJS (str): Embedded Javascript language.
        ERB (str): Embedded Ruby language.
        ERLANG (str): Erlang language.
        ESPER (str): Esper language.
        FACTOR (str): Factor language.
        FCL (str): FCL language.
        FORTH (str): Forth language.
        FORTRAN (str): Fortran language.
        FSHARP (str): F# language.
        GAS (str): Gas language.
        GHERKIN (str): Gherkin language.
        GFM (str): GitHub Flavored Markdown language.
        GITHUB_MARKDOWN (str): GitHub Flavored Markdown language.
        GO (str): Go language.
        GROOVY (str): Groovy language.
        HAML (str): HAML language.
        HASKELL (str): Haskell language.
        HASKELL_LITERATE (str): Haskell (Literate) language.
        HAXE (str): Haxe language.
        HXML (str): HXML language.
        ASP_NET (str): ASP.NET language.
        HTML (str): HTML language.
        HTTP (str): HTTP language.
        IDL (str): IDL language.
        PUG (str): Pug language.
        JAVA (str): Java language.
        JSP (str): Java Server Pages language.
        JAVASCRIPT (str): JavaScript language.
        JSON (str): JSON language.
        JSON_LD (str): JSON-LD language.
        JSX (str): JSX language.
        JINJA2 (str): Jinja2 language.
        JULIA (str): Julia language.
        KOTLIN (str): Kotlin language.
        LESS (str): LESS language.
        LIVESCRIPT (str): LiveScript language.
        LUA (str): Lua language.
        MARKDOWN (str): Markdown language.
        MIRC (str): mIRC language.
        MARIA_DB (str): MariaDB SQL language.
        MATHEMATICA (str): Mathematica language.
        MODELICA (str): Modelica language.
        MUMPS (str): MUMPS language.
        MS_SQL (str): MS SQL language.
        MBOX (str): mbox language.
        MYSQL (str): MySQL language.
        NGINX (str): Nginx language.
        NSIS (str): NSIS language.
        NTRIPLES (str): NTriples language.
        OBJ_C (str): Objective-C language.
        OCAML (str): OCaml language.
        OCTAVE (str): Octave language.
        OZ (str): Oz language.
        PASCAL (str): Pascal language.
        PEG_JS (str): PEG.js language.
        PERL (str): Perl language.
        PHP (str): PHP language.
        PIG (str): Pig language.
        PLSQL (str): PLSQL language.
        POWERSHELL (str): PowerShell language.
        INI (str): Properties files language.
        PROTOBUF (str): ProtoBuf language.
        PYTHON (str): Python language.
        PUPPET (str): Puppet language.
        QLANG (str): Q language.
        RSCRIPT (str): R language.
        RST (str): reStructuredText language.
        RPM_CHANGES (str): RPM Changes language.
        RPM_SPEC (str): RPM Spec language.
        RUBY (str): Ruby language.
        RUST (str): Rust language.
        SAS (str): SAS language.
        SASS (str): Sass language.
        SCALA (str): Scala language.
        SCHEME (str): Scheme language.
        SCSS (str): SCSS language.
        SHELL (str): Shell language.
        SIEVE (str): Sieve language.
        SLIM (str): Slim language.
        SMALLTALK (str): Smalltalk language.
        SMARTY (str): Smarty language.
        SOLR (str): Solr language.
        SML (str): SML language.
        SOY (str): Soy language.
        SPARQL (str): SPARQL language.
        SPREADSHEET (str): Spreadsheet language.
        SQL (str): SQL language.
        SQLITE (str): SQLite language.
        SQUIRREL (str): Squirrel language.
        STYLUS (str): Stylus language.
        SWIFT (str): Swift language.
        STEX (str): sTeX language.
        LATEX (str): LaTeX language.
        SYSTEM_VERILOG (str): SystemVerilog language.
        TCL (str): Tcl language.
        TEXTILE (str): Textile language.
        TIDDLYWIKI (str): TiddlyWiki language.
        TIKI_WIKI (str): Tiki Wiki language.
        TOML (str): TOML language.
        TORNADO (str): Tornado language.
        TROFF (str): troff language.
        TTCN (str): TTCN language.
        TTCN_CFG (str): TTCN_CFG language.
        TURTLE (str): Turtle language.
        TYPESCRIPT (str): TypeScript language.
        TYPESCRIPT_JSX (str): TypeScript-JSX language.
        TWIG (str): Twig language.
        WEB_IDL (str): Web IDL language.
        VB_NET (str): VB.NET language.
        VBSCRIPT (str): VBScript language.
        VELOCITY (str): Velocity language.
        VERILOG (str): Verilog language.
        VHDL (str): VHDL language.
        VUE (str): Vue.js Component language.
        XML (str): XML language.
        XQUERY (str): XQuery language.
        YACAS (str): Yacas language.
        YAML (str): YAML language.
        Z80 (str): Z80 language.
        MSCGEN (str): mscgen language.
        XU (str): xu language.
        MSGENNY (str): msgenny language.
    """

    AUTODETECT:     str = "Autodetect"
    PLAIN:          str = "Plain Text"
    APL:            str = "APL"
    PGP:            str = "PGP"
    ASN1:           str = "ASN.1"
    ASTERISK:       str = "Asterisk"
    BRAINFUCK:      str = "Brainfuck"
    CLANG:          str = "C"
    C:              str = "C"
    CPP:            str = "C++"
    COBOL:          str = "Cobol"
    CSHARP:         str = "C#"
    CLOJURE:        str = "Clojure"
    CLOJURE_SCRIPT: str = "ClojureScript"
    GSS:            str = "Closure Stylesheets (GSS)"
    CMAKE:          str = "CMake"
    COFFEE_SCRIPT:  str = "CoffeeScript"
    LISP:           str = "Common Lisp"
    CYPHER:         str = "Cypher"
    CYTHON:         str = "Cython"
    CRYSTAL:        str = "Crystal"
    CSS:            str = "CSS"
    CQL:            str = "CQL"
    DLANG:          str = "D"
    D:              str = "D"
    DART:           str = "Dart"
    DIFF:           str = "diff"
    DJANGO:         str = "Django"
    DOCKER:         str = "Dockerfile"
    DTD:            str = "DTD"
    DYLAN:          str = "Dylan"
    EBNF:           str = "EBNF"
    ECL:            str = "ECL"
    EDN:            str = "edn"
    EIFFEL:         str = "Eiffel"
    ELM:            str = "Elm"
    EJS:            str = "Embedded Javascript"
    ERB:            str = "Embedded Ruby"
    ERLANG:         str = "Erlang"
    ESPER:          str = "Esper"
    FACTOR:         str = "Factor"
    FCL:            str = "FCL"
    FORTH:          str = "Forth"
    FORTRAN:        str = "Fortran"
    FSHARP:         str = "F#"
    GAS:            str = "Gas"
    GHERKIN:        str = "Gherkin"
    GFM:            str = "GitHub Flavored Markdown"
    GITHUB_MARKDOWN: str = "GitHub Flavored Markdown"
    GO:             str = "Go"
    GROOVY:         str = "Groovy"
    HAML:           str = "HAML"
    HASKELL:        str = "Haskell"
    HASKELL_LITERATE: str = "Haskell (Literate)"
    HAXE:           str = "Haxe"
    HXML:           str = "HXML"
    ASP_NET:        str = "ASP.NET"
    HTML:           str = "HTML"
    HTTP:           str = "HTTP"
    IDL:            str = "IDL"
    PUG:            str = "Pug"
    JAVA:           str = "Java"
    JSP:            str = "Java Server Pages"
    JAVASCRIPT:     str = "JavaScript"
    JSON:           str = "JSON"
    JSON_LD:        str = "JSON-LD"
    JSX:            str = "JSX"
    JINJA2:         str = "Jinja2"
    JULIA:          str = "Julia"
    KOTLIN:         str = "Kotlin"
    LESS: str = "LESS"
    LIVESCRIPT: str = "LiveScript"
    LUA: str = "Lua"
    MARKDOWN: str = "Markdown"
    MIRC: str = "mIRC"
    MARIA_DB: str = "MariaDB SQL"
    MATHEMATICA: str = "Mathematica"
    MODELICA: str = "Modelica"
    MUMPS: str = "MUMPS"
    MS_SQL: str = "MS SQL"
    MBOX: str = "mbox"
    MYSQL: str = "MySQL"
    NGINX: str = "Nginx"
    NSIS: str = "NSIS"
    NTRIPLES: str = "NTriples"
    OBJ_C: str = "Objective-C"
    OCAML: str = "OCaml"
    OCTAVE: str = "Octave"
    OZ: str = "Oz"
    PASCAL: str = "Pascal"
    PEG_JS: str = "PEG.js"
    PERL: str = "Perl"
    PHP: str = "PHP"
    PIG: str = "Pig"
    PLSQL: str = "PLSQL"
    POWERSHELL: str = "PowerShell"
    INI: str = "Properties files"
    PROTOBUF: str = "ProtoBuf"
    PYTHON: str = "Python"
    PUPPET: str = "Puppet"
    QLANG: str = "Q"
    RSCRIPT: str = "R"
    RST: str = "reStructuredText"
    RPM_CHANGES: str = "RPM Changes"
    RPM_SPEC: str = "RPM Spec"
    RUBY: str = "Ruby"
    RUST: str = "Rust"
    SAS: str = "SAS"
    SASS: str = "Sass"
    SCALA: str = "Scala"
    SCHEME: str = "Scheme"
    SCSS: str = "SCSS"
    SHELL: str = "Shell"
    SIEVE: str = "Sieve"
    SLIM: str = "Slim"
    SMALLTALK: str = "Smalltalk"
    SMARTY: str = "Smarty"
    SOLR: str = "Solr"
    SML: str = "SML"
    SOY: str = "Soy"
    SPARQL: str = "SPARQL"
    SPREADSHEET: str = "Spreadsheet"
    SQL: str = "SQL"
    SQLITE: str = "SQLite"
    SQUIRREL: str = "Squirrel"
    STYLUS: str = "Stylus"
    SWIFT: str = "SWIFT"
    STEX: str = "sTeX"
    LATEX: str = "LaTeX"
    SYSTEM_VERILOG: str = "SystemVerilog"
    TCL: str = "Tcl"
    TEXTILE: str = "Textile"
    TIDDLYWIKI: str = "TiddlyWiki"
    TIKI_WIKI: str = "Tiki Wiki"
    TOML: str = "TOML"
    TORNADO: str = "Tornado"
    TROFF: str = "troff"
    TTCN: str = "TTCN"
    TTCN_CFG: str = "TTCN_CFG"
    TURTLE: str = "Turtle"
    TYPESCRIPT: str = "TypeScript"
    TYPESCRIPT_JSX: str = "TypeScript-JSX"
    TWIG: str = "Twig"
    WEB_IDL: str = "Web IDL"
    VB_NET: str = "VB.NET"
    VBSCRIPT: str = "VBScript"
    VELOCITY: str = "Velocity"
    VERILOG: str = "Verilog"
    VHDL: str = "VHDL"
    VUE: str = "Vue.js Component"
    XML: str = "XML"
    XQUERY: str = "XQuery"
    YACAS: str = "Yacas"
    YAML: str = "YAML"
    Z80: str = "Z80"
    MSCGEN: str = "mscgen"
    XU: str = "xu"
    MSGENNY: str = "msgenny"
