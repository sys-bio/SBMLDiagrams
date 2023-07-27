import tellurium as te
import SBMLDiagrams

r = te.loada('''
//Created by libAntimony v2.5
model *Jana_WolfGlycolysis()

  // Compartments and Species:
  compartment compartment_;
  species Glucose in compartment_, fructose_1_6_bisphosphate in compartment_;
  species glyceraldehyde_3_phosphate in compartment_, glycerate_3_phosphate in compartment_;
  species pyruvate in compartment_, Acetyladehyde in compartment_, External_acetaldehyde in compartment_;
  species ATP in compartment_, ADP in compartment_, NAD in compartment_, NADH in compartment_;
  species $External_glucose in compartment_, $ethanol in compartment_, $Glycerol in compartment_;
  species $Sink in compartment_;

  // Reactions:    
  J0: $External_glucose => Glucose; J0_inputFlux;
  J1: Glucose + 2ATP => fructose_1_6_bisphosphate + 2ADP; J1_k1*Glucose*ATP*(1/(1 + (ATP/J1_Ki)^J1_n));
  J2: fructose_1_6_bisphosphate => glyceraldehyde_3_phosphate + glyceraldehyde_3_phosphate; J2_J2_k*fructose_1_6_bisphosphate;
  J3: glyceraldehyde_3_phosphate + NADH => NAD + $Glycerol; J3_J3_k*glyceraldehyde_3_phosphate*NADH;
  J4: glyceraldehyde_3_phosphate + ADP + NAD => ATP + glycerate_3_phosphate + NADH; (J4_kg*J4_kp*glyceraldehyde_3_phosphate*NAD*ADP - J4_ka*J4_kk*glycerate_3_phosphate*ATP*NADH)/(J4_ka*NADH + J4_kp*ADP);
  J5: glycerate_3_phosphate + ADP => ATP + pyruvate; J5_J5_k*glycerate_3_phosphate*ADP;
  J6: pyruvate => Acetyladehyde; J6_J6_k*pyruvate;
  J7: Acetyladehyde + NADH => NAD + $ethanol; J7_J7_k*Acetyladehyde*NADH;
  J8: Acetyladehyde => External_acetaldehyde; J8_J8_k1*Acetyladehyde - J8_J8_k2*External_acetaldehyde;
  J9: ATP => ADP; J9_J9_k*ATP;
  J10: External_acetaldehyde => $Sink; J10_J10_k*External_acetaldehyde;

  // Species initializations:
  Glucose = 0;
  fructose_1_6_bisphosphate = 0;
  glyceraldehyde_3_phosphate = 0;
  glycerate_3_phosphate = 0;
  pyruvate = 0;
  Acetyladehyde = 0;
  External_acetaldehyde = 0;
  ATP = 3;
  ADP = 1;
  NAD = 0.5;
  NADH = 0.5;
  External_glucose = 0;
  ethanol = 0;
  Glycerol = 0;
  Sink = 0;

  // Compartment initializations:
  compartment_ = 1;

  // Variable initializations:
  J0_inputFlux = 50;
  J1_k1 = 550;
  J1_Ki = 1;
  J1_n = 4;
  J2_J2_k = 9.8;
  J3_J3_k = 85.7;
  J4_kg = 323.8;
  J4_kp = 76411.1;
  J4_ka = 57823.1;
  J4_kk = 23.7;
  J5_J5_k = 80;
  J6_J6_k = 9.7;
  J7_J7_k = 2000;
  J8_J8_k1 = 375;
  J8_J8_k2 = 375;
  J9_J9_k = 28;
  J10_J10_k = 80;
  J2_k = 9.8;
  J3_k = 85.7;
  J5_k = 80;
  J6_k = 9.7;
  J7_k = 2000;
  J8_k1 = 375;
  J8_k2 = 375;
  J9_k = 28;
  J10_k = 80;

  //Other declarations:
  const compartment_, J0_inputFlux, J1_k1, J1_Ki, J1_n, J2_J2_k, J3_J3_k;
  const J4_kg, J4_kp, J4_ka, J4_kk, J5_J5_k, J6_J6_k, J7_J7_k, J8_J8_k1, J8_J8_k2;
  const J9_J9_k, J10_J10_k, J2_k, J3_k, J5_k, J6_k, J7_k, J8_k1, J8_k2, J9_k;
  const J10_k;
end
''')
sbmlStr = r.getSBML()
df = SBMLDiagrams.load(sbmlStr)
df.autolayout(layout="spectral", scale = 500)
df.draw(output_fileName="spectral.png")

df.autolayout(layout="spring", scale = 500, k = 2)
df.draw(output_fileName="spring.png")

df.autolayout(layout="circular", scale = 500)
df.draw(output_fileName="circular.png")

#df.autolayout(layout="random")
#df.draw(output_fileName="random.png")

#df.autolayout(layout="graphviz")
#df.draw(output_fileName="graphviz_dot.png")

#df.autolayout(layout="graphviz", graphvizProgram = 'neato')
#df.draw(output_fileName="graphviz_neato.png")
