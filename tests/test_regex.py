import unittest

from simple_animl.utils.regex import NC_NAME


class TestRegex(unittest.TestCase):
    def test_NCName_OK(self):
        tests = [
            "alpha",
            "beta_gamma",
            "delta.alpha",
            "epsilon-beta",
            "zeta",
            "eta_theta",
            "iota.kappa",
            "lambda-mu",
            "nu",
            "xi_omicron",
            "pi.rho",
            "sigma-tau",
            "upsilon",
            "phi_chi",
            "psi.omega",
            "Alpha-Beta",
            "Gamma",
            "Delta_Epsilon",
            "Zeta.Eta",
            "Theta-Iota",
        ]

        for test in tests:
            with self.subTest(test=test):
                self.assertRegex(test, NC_NAME)

    def test_NCName_NOK(self):
        tests = [
            ("delta,alpha", "Contains a comma"),
            ("iota,kappa", "Contains a comma"),
            ("pi,rho", "Contains a comma"),
            ("psi,omega", "Contains a comma"),
            ("Zeta,Eta", "Contains a comma"),
            ("beta gamma", "Contains a space"),
            ("Delta Epsilon", "Contains a space"),
            ("eta theta", "Contains a space"),
            ("phi chi", "Contains a space"),
            ("xi omicron", "Contains a space"),
            ("Alpha#Beta", "Contains a special character"),
            ("epsilon#beta", "Contains a special character"),
            ("lambda#mu", "Contains a special character"),
            ("sigma#tau", "Contains a special character"),
            ("Theta#Iota", "Contains a special character"),
            ("", "Empty string"),
            (" ", "Only a space"),
            ("123", "Only numbers"),
            ("123alpha", "Starts with a number"),
            ("123Gamma", "Starts with a number"),
        ]

        for test in tests:
            with self.subTest(test=f"{test[1]}: '{test[0]}'"):
                self.assertNotRegex(test[0], NC_NAME)
