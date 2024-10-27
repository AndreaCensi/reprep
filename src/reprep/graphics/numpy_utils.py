from numpy import isfinite, isinf, isnan


def assert_finite(a):
    if not isfinite(a).all():  # XXX inefficeint
        n = len(a.flat)
        n_nan = (1 * isnan(a)).sum()
        n_inf = (1 * isinf(a)).sum()

        raise ValueError("Some values are not finite. Nan: {}/{} Inf: {}/{}".format(n_nan, n, n_inf, n))
