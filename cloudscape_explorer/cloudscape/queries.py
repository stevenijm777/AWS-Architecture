import pandas as pd


def calculate_2d_cooccurence_df_plus_listofmore(
    elements, rc_names, f_extract_listofstr_from_elem
):
    morethan2 = []
    num_with_2 = 0
    num_with_1 = 0
    df = pd.DataFrame(0, index=rc_names + ["Total"], columns=rc_names)
    for elem in elements:
        attr = f_extract_listofstr_from_elem(elem)
        # assert len(attr) > 0
        if len(attr) == 0:
            continue
        elif len(attr) == 1:
            c0 = attr[0]
            df.loc[c0, c0] += 1
            num_with_1 += 1
        elif len(attr) == 2:
            c1, c2 = attr
            df.loc[c1, c2] += 1
            df.loc[c2, c1] += 1
            num_with_2 += 1
        else:
            morethan2.append(elem)

    df.loc["Total"] = df.sum(axis=1)

    n = len(elements)
    df = df.map(lambda x: f"{(x*100)//n}% ({x})")

    return df, morethan2, num_with_1, num_with_2


def normalize_dict(d, n):
    return {k: v / n * 100 for k, v in d.items()}
