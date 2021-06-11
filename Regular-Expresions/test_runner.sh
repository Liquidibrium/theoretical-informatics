#!/bin/bash
# shellcheck disable=SC2028


P="^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^{ PASSED: "
T="+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++{ TRUE: "
F="-------------------------------------------------------------------{ FALSE: "

Ctr=0; fullAmount=" / 20"
Sep="*****************************"

post00="00.txt"; post01="01.txt"; post02="02.txt"; post03="03.txt"; post04="04.txt"
post05="05.txt"; post06="06.txt"; post07="07.txt"; post08="08.txt"; post09="09.txt"
post10="10.txt"; post11="11.txt"; post12="12.txt"; post13="13.txt"; post14="14.txt"
post15="15.txt"; post16="16.txt"; post17="17.txt"; post18="18.txt"; post19="19.txt"


runFn() {
  RUN="python3 run_ganj.py "
  inFPPre="Public tests/P2/In (public)/in"
  currPost=$1

  echo "${Sep} ${currPost} ${Sep}" &&
  $RUN "${inFPPre}${currPost}" && echo ""
}

diffFn() {
  DIFF="diff "
  outFPPre="Public tests/P2/Out (public)/out"
  outMyFPPre="Public tests/P2/Out_My/out_my"
  currPost=$1

  echo "${Sep} ${currPost} ${Sep}" &&
  if $DIFF "${outFPPre}${currPost}" "${outMyFPPre}${currPost}";
  then Ctr=$((Ctr+1)) && echo "${T}${currPost}";
  else echo "${F}${currPost}";
  fi  && echo ""
}

runAllFn() {
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: RUN BEGIN :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
  runFn $post00;
  runFn $post01;
  runFn $post02;
  runFn $post03;
  runFn $post04;
  runFn $post05;
  runFn $post06;
  runFn $post07;
  runFn $post08;
  runFn $post09;
  runFn $post10;
  runFn $post11;
  runFn $post12;
  runFn $post13;
  runFn $post14;
  runFn $post15;
  runFn $post16;
  runFn $post17;
  runFn $post18;
  runFn $post19;
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: RUN END :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
}

diffAllFn() {
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: DIFF BEGIN :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
  diffFn $post00;
  diffFn $post01;
  diffFn $post02;
  diffFn $post03;
  diffFn $post04;
  diffFn $post05;
  diffFn $post06;
  diffFn $post07;
  diffFn $post08;
  diffFn $post09;
  diffFn $post10;
  diffFn $post11;
  diffFn $post12;
  diffFn $post13;
  diffFn $post14;
  diffFn $post15;
  diffFn $post16;
  diffFn $post17;
  diffFn $post18;
  diffFn $post19;
  echo "${P}$Ctr${fullAmount}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: DIFF END :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
}



runAllFn;
diffAllFn;
