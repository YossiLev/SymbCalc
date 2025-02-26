import sympy as sp

# Define symbolic variables
t, z = sp.symbols('t z')
# A_coeffs = sp.symbols('S0 S1 S2 S3', cls=sp.Function)
# B_coeffs = sp.symbols('I0 I1 I2 I3', cls=sp.Function)
# C_coeffs = sp.symbols('P0 P1 P2 P3', cls=sp.Function)

# A_coeffs = list(map(lambda x : x(t), A_coeffs))
# B_coeffs = list(map(lambda x : x(t), B_coeffs))
# C_coeffs = list(map(lambda x : x(t), C_coeffs))

A_coeffs = list(map(lambda x : sp.Function(f"S{x}")(t), range(4)))
B_coeffs = list(map(lambda x : sp.Function(f"I{x}")(t), range(4)))
C_coeffs = list(map(lambda x : sp.Function(f"P{x}")(t), range(4)))

A_coeffs[0], B_coeffs[0], C_coeffs[0] = 0, 0, 100
# Define time-dependent power series expansions
A_series = sum(A_coeffs[n] * z**n for n in range(4))
B_series = sum(B_coeffs[n] * z**n for n in range(4))
C_series = sum(C_coeffs[n] * z**n for n in range(4))

# Compute time derivatives
dA_dt = sp.diff(A_series, t)
dB_dt = sp.diff(B_series, t)
dC_dt = sp.diff(C_series, t)

# Define example functions F(B, C, g), G(A, C, g), H(A, B, g)
F_expr = B_series * C_series 
G_expr = A_series * C_series 
H_expr = A_series * B_series 

# Expand both sides in powers of z
lhs_A = sp.expand(dA_dt)
rhs_A = sp.expand(F_expr)
lhs_B = sp.expand(dB_dt)
rhs_B = sp.expand(G_expr)
lhs_C = sp.expand(dC_dt)
rhs_C = sp.expand(H_expr)

# Separate equations by powers of g
num_terms = 4  # Number of orders to compute



eqs = []

for n in range(1, 3):
    eqs.append(sp.Eq(lhs_A.coeff(z, n), rhs_A.coeff(z, n)))
    eqs.append(sp.Eq(lhs_B.coeff(z, n), rhs_B.coeff(z, n)))
    eqs.append(sp.Eq(lhs_C.coeff(z, n), rhs_C.coeff(z, n)))


# Convert to LaTeX with new lines
print(r"\begin{aligned}" + " \\\\ ".join(sp.latex(expr) for expr in eqs) + r"\end{aligned}")

# for eq in eqs:
#     print(sp.latex(eq))
# Solve for the unknown coefficents
ics = {A_coeffs[1].subs(t, 0): 1, B_coeffs[1].subs(t, 0): 2, C_coeffs[1].subs(t, 0): 0,}
    # A_coeffs[2].subs(t, 0): 0, B_coeffs[2].subs(t, 0): 0, C_coeffs[2].subs(t, 0): 1
    # }

solution = sp.dsolve(eqs[:3], ics={A_coeffs[1].subs(t, 0): 1, B_coeffs[1].subs(t, 0): 2, C_coeffs[1].subs(t, 0): 0,})

print(r"\begin{aligned}" + " \\\\ ".join(sp.latex(expr) for expr in solution) + r"\end{aligned}")

solution = sp.dsolve(eqs[3:], ics={A_coeffs[2].subs(t, 0): 0, B_coeffs[2].subs(t, 0): 0, C_coeffs[2].subs(t, 0): 1,})



# Display results
# for sol in solution:
#     for key, val in sol.items():
#         print("")
#         print(f"{key} =", val)
