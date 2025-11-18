from sympy import *
P, D, t, hoop = symbols('P, D, t, hoop')
#hoop = P * D / 2 / t
barlow_eq = Eq(P * D / 2 / t, hoop)
barlow_eq = Eq(hoop, P * D / 2 / t)

solns = solve(barlow_eq, t)
soln = solns[0]

params = {
  "P": 150.0e5,
  "D": 24 * 25.4 * 1.e-3,
  "SMYS": 450.0e6,
  "Df": 0.72,
  "t_nom": 15.9 * 1.e-3,
}

params = {
  "P": 150.0e5,
  "D": 24 * 25.4 * 1.e-3,
  "t": 15.9 * 1.e-3,
  "test": 0.0
}

hoop1 = barlow_eq.evalf(subs=params)
# sympify(barlow_eq).evalf(subs=params)

