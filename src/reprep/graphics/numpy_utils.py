from numpy import isnan, isinf, isfinite


def assert_finite(a):
    if  isfinite(a).all():
        return

    n = len(a.flat)
    n_nan = (1 * isnan(a)).sum()
    n_inf = (1 * isinf(a)).sum()
    msg = ('Some values are not finite. Nan: %s/%s Inf: %s/%s' %
        (n_nan, n, n_inf, n))
    raise ValueError(msg)




