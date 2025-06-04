# code generators
import sympy as sp
import traceback

from sympy.printing.numpy import NumPyPrinter
class SetfosPythonCodePrinter(NumPyPrinter):
   def __init__(self):
      super().__init__()
      #self._print_Derivative = None

   def _print_Symbol(self, expr):
      #for line in traceback.format_stack():
      #   print(line.strip())

      name = super()._print_Symbol(expr)
      if '\\' in name:   # Remove curly braces from subscripted variables
            name = name.replace('\\', '')

      if ',' in name:
            name = name.replace(',', '_')

      if name == "lambda":
         return "lam"

      if name == "R_0_ n":
         return "R_0_n"

      if name == "R_0_ p":
         return "R_0_p"

      if name == "mu_0_ n":
         return "mu_0_n"

      if name == "mu_0_ p":
         return "mu_0_p"

      if name == "N_0_ n":
         return "N_0_n"

      if name == "N_0_ p":
         return "N_0_p"

      if name == "E_mathrmgap":
         return "E_gap"

      return name

   def _print_IndexedBase(self, expr):
      name = super()._print_Symbol(expr)
      if '\\' in name:
            name = name.replace('\\', '')

      if '^' in name:
            name = name.replace('^', '_')

      return name

   def _print_Derivative(self, expr):
      #print("Printing function {}.".format(sp.srepr(expr)))
      return "dummy"

   def _print_Subs(self, obj):
       expr, old, new = obj.args
       #print("Printing subs {}.".format(sp.srepr(expr)))
       #print("Printing subs new {}.".format(sp.srepr(new[0])))

       assert(expr.func == sp.Derivative)
       funcName = super()._print_Symbol(expr.args[0].func)
       #print("Function name is '{}'".format(funcName))

       knownFunctions = {'B': "bernoulliprime"}

       return knownFunctions[funcName] + "("+self._print(new[0]) + ")"

   def _print_Function(self, expr):
      #print("Printing function {}.".format(sp.srepr(expr)))
      #for line in traceback.format_stack():
      #   print(line.strip())

      name = super()._print_Symbol(expr)

      knownFunctions = {'B': "bernoulli"}

      funName = knownFunctions[name]

      args = expr.args[0]

      return funName + "(" + self._print(args) + ")"


   def _print_Indexed(self, expr):
      base, index = expr.args
      if index.func == sp.Add:
         #print("Add:" + sp.srepr(index))
         a, b = index.args
         #print("arg1:",sp.srepr(a) )
         #print("arg2:",sp.srepr(b) )
         assert(a.func == sp.Idx or b.func == sp.Idx)
         assert(a.func == sp.Idx or a.func == sp.core.numbers.One or a.func == sp.core.numbers.NegativeOne or a.func == sp.Rational or a.func == sp.core.numbers.Half)
         assert(b.func == sp.Idx or b.func == sp.core.numbers.One or b.func == sp.core.numbers.NegativeOne or b.func == sp.Rational or b.func == sp.core.numbers.Half)
         if a.func == sp.Idx:
            indexarg = a
            offsetarg = b
         else:
            indexarg = b
            offsetarg = a

         if offsetarg.func == sp.core.numbers.One:
            indexstring = '[2:]'
         elif offsetarg.func == sp.core.numbers.NegativeOne:
            indexstring = '[:-2]'
         elif offsetarg.func == sp.core.numbers.Half:
            assert(offsetarg.denominator == 2)
            indexstring = '[1:]'
         elif offsetarg.func == sp.Rational:
            assert(offsetarg.numerator == -1)
            assert(offsetarg.denominator == 2)
            indexstring = '[:-1]'

      elif index.func == sp.Idx:
         indexstring = '[1:-1]'
      else:
         print(srepr(index))
         raise AssertionError("Index must be of form 'i', 'i+1', 'i+1/2'.")

      return self._print(base)+indexstring

