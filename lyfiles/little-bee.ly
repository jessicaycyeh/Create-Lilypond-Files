\version "2.20.0"  % necessary for upgrading to future LilyPond versions.

\header{
  title = "Little Bee"
}




% Piano+Guitar 
  
%\layout { \omit Voice.StringNumber }
\new StaffGroup <<
   \new Staff \relative {
     \clef "treble_8"
     \time 4/4
     c16 d e f g4
     c,16\5 d\5 e\4 f\4 g4\4
     c,16 d e f g4
   }
   \new TabStaff \relative {
     c16 d e f g4
     c,16\5 d\5 e\4 f\4 g4\4
     \set TabStaff.minimumFret = #5
     \set TabStaff.restrainOpenStrings = ##t
     c,16 d e f g4
   }
>>


%{
% Two staves
<<
  \new Staff \relative{ \clef "treble"
              \key c \major
              \time 4/4
              \tempo "Andante" 4 = 120
               g' e <e c>2| f4 d d2| c4( d e f)|g g g2 \bar "|." }

  \new Staff \relative { \clef "bass" \key c \major \time 4/4
               c1|g|c|c \bar "|." }
>>
%}

% Fretted strings
%{
\new TabStaff \relative {
  a,8 a' <c e> a
  d,8 a' <d f> a
}
%}






%{
%Single staff, multiple voices
<<
\relative { c'' d e}
\\
\relative { c' d e}
>>
%}

