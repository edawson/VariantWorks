import cudf
import variantworks as vw


def _merge(a, b, columns=[], sample_columns=[], join="outer", inplace=True):
    """
    Base merge function.
    """
    columns.extend(sample_columns)
    return a.merge(b, on=columns, how=join)


def _count_overlaps(a, b, columns=[], dest="counts", join="outer", inplace=True):
    """
    A modification of the base merge function that
    creates a column <dest> which contains counts of the
    number of overlaps of <a> and <b> when joining by <columns>
    """
    return


def merge_by_start_position(a, b, join="outer", inplace=True):
    return _merge(a, b, columns=["chrom", "start_position"], join=join)


def merge_by_start_and_end_position(a, b, join="outer", sample_columns=[]):
    return _merge(a, b, columns=["chrom", "start_pos", "end_pos"], join=join)


def merge_by_alleles(a, b, join="outer"):
    return _merge(a, b, columns=["chrom", "start_pos", "end_pos", "ref", "alt"], join=join)


def merge_by_germline_alleles(a, b, join="outer"):
    return _merge(a, b, columns=["chrom", "start_pos", "end_pos", "ref", "alt"], sample_columns=["normal"], join=join)


def merge_by_somatic_alleles(a, b, join="outer"):
    return _merge(a, b, columns=["chrom", "start_pos", "end_pos", "ref", "alt"], sample_columns=["tumor", "normal"], join="join")


def sum_callers(a, caller_columns):
    a["n_callers"] = a[caller_columns].sum(axis=1)
    return a


def minimum_caller_consensus(a, caller_columns=[], min_callers=2):
    a = sum_callers(a)
    return a.query("n_callers" >= min_callers)


def mutations_per_sample(a, sample_columns=[]):
    return a[sample_columns].value_counts()