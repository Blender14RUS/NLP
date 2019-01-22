import pandas as pd
from sklearn.cluster import KMeans, MeanShift
from sklearn.metrics import f1_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

DATASET_STEPS_FILENAME = "dataset_steps.csv"
DATASET_EVENTS_FILENAME = "dataset_events.csv"


def read_dataset(filename):
    dataset = pd.read_csv(filename).values

    return dataset


def divide_dataframe(dataframe):
    attrs = dataframe[:, 1:-1]
    classes = dataframe[:, -1]
    lb = LabelEncoder()
    classes = lb.fit_transform(classes)

    return attrs, classes


def kmeans(x_train, y_train, x_test, y_test, range_clusters):
    for n_clusters in range_clusters:
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(x_train, y_train)
        y_pred = kmeans.fit_predict(x_test)
        print('kmeans n_clusters = {} f1_score = {}'
              .format(n_clusters, str(f1_score(y_test, y_pred, average='micro'))))


def gaussian_mixture(x_train, y_train, x_test, y_test, af):
    af.fit(x_train, y_train)
    y_pred = af.predict(x_test)
    print('gaussian mixture ' + str(f1_score(y_test, y_pred, average="micro")))


def mean_shift(x_train, y_train, x_test, y_test, range_bandwidth):
    for n_bandwidth in range_bandwidth:
        ms = MeanShift(bandwidth=n_bandwidth)
        ms.fit(x_train, y_train)
        y_pred = ms.predict(x_test)
        print('mean shift n_bandwidth = {}, f1_score = {}'
              .format(n_bandwidth, str(f1_score(y_test, y_pred, average='micro'))))


def kmeans_silhouette(df):
    range_clusters = [2, 3, 4, 5, 6, 8, 10]
    for n_clusters in range_clusters:
        kmeans = KMeans(n_clusters=n_clusters)
        preds = kmeans.fit_predict(df)
        score = silhouette_score(df, preds, metric='euclidean')
        print("kmeans n_clusters = {}, silhouette_score = {})".format(n_clusters, score))


def main():
    dataframe = read_dataset(DATASET_EVENTS_FILENAME)
    attrs, classes = divide_dataframe(dataframe)
    x_train, x_test, y_train, y_test = train_test_split(attrs, classes, test_size=0.3, random_state=55)

    print('*' * 100)
    kmeans(x_train, y_train, x_test, y_test, [2, 3, 4, 5, 6, 8, 10])
    print('*' * 100)
    kmeans_silhouette(attrs)
    print('*' * 100)
    gaussian_mixture(x_train, y_train, x_test, y_test,
                     GaussianMixture(n_components=3, covariance_type="full", tol=0.01))
    gaussian_mixture(x_train, y_train, x_test, y_test,
                     GaussianMixture(n_components=2, covariance_type="full"))
    gaussian_mixture(x_train, y_train, x_test, y_test,
                     GaussianMixture(n_components=5, covariance_type="diag"))
    print('*' * 100)
    mean_shift(x_train, y_train, x_test, y_test, [2, 10, 1, 0.2, 60])
    print('*' * 100)

    visualization(x_train, y_train, x_test)



def visualization(x_train, y_train, x_test):
    # K-Means --------------------------------------------------------------
    kmeans_model = KMeans(n_clusters=10, init='k-means++')
    X = kmeans_model.fit(x_train, y_train)
    labels=kmeans_model.labels_.tolist()

    l = kmeans_model.fit_predict(x_test)
    pca = PCA(n_components=16).fit(x_train, y_train)

    datapoint = pca.transform(x_train)
    print(datapoint[:, 0])
    print(datapoint[:, 1])
    print(datapoint[:, 1].max())

    print(len(datapoint))

    print(x_train[56])
    print(x_train[44])
    print(x_train[67])
    print(x_train[4])

    plt.figure
    label1 = ["#FF0000", "#00FF00", "#0000FF", "#800080", "#7A0760", "#C8461C", "#A61FF7", "#9E17E2", "#AE0D02", "#67C6F3", "#7CBB2D", "#7C39B2", "#1412C0", "#46E54E", "#7A6415"	, "#791343"	, "#0C046B"	, "#67079C"	, "#8E2647"]
    color = [label1[i] for i in labels]
    plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)

    centroids = kmeans_model.cluster_centers_
    centroidpoint = pca.transform(centroids)
    plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=50, c='#000000')
    plt.show()

    # # Agglomerative Clustering--------------------------------------------------------------
    # # create dendrogram
    # dendrogram = sch.dendrogram(sch.linkage(x_train, method='ward'))
    # # create clusters
    # hc = AgglomerativeClustering(n_clusters=10, affinity = 'euclidean', linkage = 'complete')
    # X = hc.fit(x_train)
    # # save clusters for chart
    # y_hc = hc.fit_predict(x_train)
    # plt.show()


if __name__ == "__main__":
    main()