import polars as pl
from wonderwords import RandomSentence
import pytest
from polars_casing import Casing  # noqa: F401, F403

SIZES = [10, 100, 1000, 10000]


def get_df(N: int = 1000) -> pl.DataFrame:
    s = RandomSentence()

    return pl.DataFrame(
        {
            "random_sentence": [s.sentence() for _ in range(N)],
        }
    )


def to_pascal_case(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pascal_case=pl.col("random_sentence").casing.pascal_case(),
    )


@pytest.mark.benchmark(group="pascal")
@pytest.mark.parametrize("N", SIZES)
def test_polars_pascal_casing(benchmark, N):
    df = get_df(N)
    benchmark(to_pascal_case, df)


@pytest.mark.benchmark(group="pascal")
@pytest.mark.parametrize("N", SIZES)
def test_naive_python_pascal_casing(benchmark, N):
    df = get_df(N)
    benchmark(
        lambda df: df.with_columns(
            pascal_case=pl.col("random_sentence").map_elements(
                lambda x: "".join([i.title() for i in x.split(" ")])
            )
        ),
        df,
    )


@pytest.mark.benchmark(group="snake")
@pytest.mark.parametrize("N", SIZES)
def test_polars_snake_casing(benchmark, N):
    df = get_df(N)
    benchmark(
        lambda df: df.with_columns(
            snake_case=pl.col("random_sentence").casing.snake_case(),
        ),
        df,
    )


@pytest.mark.benchmark(group="snake")
@pytest.mark.parametrize("N", SIZES)
def test_naive_python_snake_casing(benchmark, N):
    df = get_df(N)
    benchmark(
        lambda df: df.with_columns(
            snake_case=pl.col("random_sentence").map_elements(
                lambda x: "_".join([i.lower() for i in x.split(" ")])
            )
        ),
        df,
    )
