def test(path: Path):

    # filenames = Read.filenames(path.input)

    # for filename in filenames:
    #     data = Read.data(path.input + filename)

    #     plot_config = {"filename": Convert.filename(filename),
    #                    "path": path.output+"test/"}


    #     Test.silhouette_score(data, plot_config=plot_config)

    filename = path.input+"pivot.pickle"

    data = Read.pickle(filename)
    data.drop(["END_TM"], axis=1, inplace=True)

    plot_config = {"filename": Convert.filename(filename),
                   "path": path.output + "test/"}
    Test.silhouette_score(data, plot_config=plot_config)
