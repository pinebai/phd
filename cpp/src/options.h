#ifndef OPTIONS_H
#define OPTIONS_H

const bool NO_CORNERS = true;

const bool VISCOUS = true;
const bool THERMAL = true;
const bool MULTI = false;
const bool REACTIVE = false;
const int LSET = 1;

const int N = 3; // Order of accuracy

const int V = 5 + int(VISCOUS) * 9 + int(THERMAL) * 3 + int(REACTIVE) +
              int(MULTI) * 2 + LSET;

// WENO Constants //
const double LAMS = 1.;   // WENO side stencil weighting
const double LAMC = 1e3;  // WENO central stencil weighting
const double EPS = 1e-14; // WENO epsilon parameter

// DG Constants //
const int DG_IT = 50;       // No. of iterations of non-Newton solver attempted
const double DG_TOL = 1e-8; // Convergence tolerance

#endif // OPTIONS_H
