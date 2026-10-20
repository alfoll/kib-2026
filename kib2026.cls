\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{kib2026}[2026/10/20 Unofficial KIB 2026 template]
\newif\ifkibdraftfont
\DeclareOption{draftfont}{\kibdraftfonttrue}
\ProcessOptions\relax
\LoadClass[10pt]{article}
\RequirePackage{iftex}
\ifXeTeX\else
  \ClassError{kib2026}{Compile with XeLaTeX}{Use python scripts/build.py}\fi
\RequirePackage[paperwidth=148mm,paperheight=210mm,top=23mm,bottom=25mm,
  left=17mm,right=18mm,headheight=0mm,headsep=10.5mm,footskip=12.5mm]{geometry}
\RequirePackage{fontspec}
\ifkibdraftfont
  \setmainfont{DejaVu Serif}
  \newfontfamily\cyrillicfont{DejaVu Serif}
  \ClassWarningNoLine{kib2026}{PREVIEW ONLY: not Times New Roman}
\else
  \IfFileExists{fonts/times.ttf}{
    \setmainfont{times.ttf}[Path=fonts/,BoldFont=timesbd.ttf,
      ItalicFont=timesi.ttf,BoldItalicFont=timesbi.ttf]
    \newfontfamily\cyrillicfont{times.ttf}[Path=fonts/,BoldFont=timesbd.ttf,
      ItalicFont=timesi.ttf,BoldItalicFont=timesbi.ttf]
  }{
    \IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}
      \newfontfamily\cyrillicfont{Times New Roman}}{
      \ClassError{kib2026}{Times New Roman is required}{Install the four Times New Roman faces or put licensed font files in fonts/. No automatic substitution is permitted.}
    }
  }
\fi
\RequirePackage{polyglossia}
\setdefaultlanguage{russian}
\setotherlanguage{english}
\RequirePackage{amsmath,amssymb,fix-cm}
\RequirePackage{graphicx,booktabs,array,indentfirst}
\RequirePackage{caption}
\RequirePackage{xurl}
\RequirePackage[hidelinks,unicode]{hyperref}
\urlstyle{same}
\pagestyle{empty}
\setlength{\parindent}{5mm}
\setlength{\parskip}{0pt}
\linespread{1}
% bp = 1/72 inch: the point unit used by Word, unlike TeX pt (1/72.27 inch).
% Single spacing = normal single baseline, without additional stretch.
\renewcommand{\normalsize}{\fontsize{10bp}{12bp}\selectfont
  \abovedisplayskip=6bp \belowdisplayskip=6bp
  \abovedisplayshortskip=3bp \belowdisplayshortskip=3bp}
\normalsize
\setlength{\emergencystretch}{1em}
\newcommand{\kibblank}[1]{\par{\fontsize{#1bp}{#1bp}\selectfont\noindent\strut\par}}
\newcommand{\kibudc}[1]{\par{\fontsize{9bp}{10.8bp}\selectfont\noindent УДК #1\par}}
\newcommand{\kibauthors}[1]{\par{\centering\fontsize{11bp}{13.2bp}\selectfont #1\par}}
\newcommand{\kibaffiliations}[1]{\par{\centering\fontsize{9bp}{10.8bp}\selectfont\itshape #1\par}}
\newcommand{\kibtitle}[1]{\kibblank{10}{\centering\fontsize{11bp}{13.2bp}\selectfont\bfseries\MakeUppercase{#1}\par}\kibblank{10}}
\newbox\kibabstractbox
\newcount\kibabstractlines
\newenvironment{kibabstract}{
  \setbox\kibabstractbox=\vbox\bgroup
  \hsize=\textwidth\linewidth=\textwidth
  \fontsize{9bp}{10.8bp}\selectfont\ignorespaces
}{\par\global\kibabstractlines=\prevgraf\egroup
  \typeout{KIB-ABSTRACT-LINES: \the\kibabstractlines}
  \ifnum\kibabstractlines<5 \ClassWarningNoLine{kib2026}{Abstract must have 5--8 lines}\fi
  \ifnum\kibabstractlines>8 \ClassWarningNoLine{kib2026}{Abstract must have 5--8 lines}\fi
  \box\kibabstractbox\kibblank{10}\normalsize}
\renewcommand{\section}{\@startsection{section}{1}{0pt}{6bp}{3bp}
  {\centering\fontsize{10bp}{12bp}\selectfont\bfseries}}
\setcounter{secnumdepth}{0}
\providecommand{\kibLastFigures}{0}
\providecommand{\kibLastTables}{0}
\DeclareCaptionFont{kibnine}{\fontsize{9bp}{10.8bp}\selectfont}
\DeclareCaptionLabelFormat{kibfigure}{Рис\ifnum\kibLastFigures>1\relax.~#2\fi}
\DeclareCaptionLabelFormat{kibtable}{Таблица\ifnum\kibLastTables>1\relax~#2\fi}
\captionsetup{font=kibnine,labelfont=normalfont,textfont=normalfont,labelsep=period,skip=3bp}
\captionsetup[figure]{labelformat=kibfigure,justification=centering,singlelinecheck=false}
\captionsetup[table]{labelformat=kibtable,justification=raggedleft,singlelinecheck=false,position=top}
\newcommand{\figref}[1]{рис.\ifnum\kibLastFigures>1\relax~\ref{#1}\fi}
\newcommand{\tabref}[1]{табл.\ifnum\kibLastTables>1\relax~\ref{#1}\fi}
\AtEndDocument{
  \immediate\write\@auxout{\string\gdef\string\kibLastFigures{\arabic{figure}}}
  \immediate\write\@auxout{\string\gdef\string\kibLastTables{\arabic{table}}}
}
\renewenvironment{thebibliography}[1]{
  \kibblank{8}
  {\centering\fontsize{8bp}{9.6bp}\selectfont\itshape Список литературы\par}
  \kibblank{8}\fontsize{8bp}{9.6bp}\selectfont
  \list{\arabic{enumiv}.}{\usecounter{enumiv}\setlength{\labelwidth}{1.5em}
    \setlength{\labelsep}{0.4em}\setlength{\leftmargin}{1.9em}
    \setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}\setlength{\topsep}{0pt}}
  \sloppy
}{\endlist\normalsize}
\endinput
