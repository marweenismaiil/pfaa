import cv2
import numpy as np
import scipy.ndimage
import joblib
from tools import *
from ml import *
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--mode', '-mode', help="Mode : train or predict", type=str)
parser.add_argument('--a', '-algorithm', help="algorithm/model name", type=str)
parser.add_argument('--i', '-image', help="licence plate to read", type=str)
parser.add_argument('--model', '-model', help="Model file path", type=str)
parser.add_argument('--d', '-dataset', help="dataset folder path", type=str)

args = parser.parse_args()


if args.mode == "train":

    # Load Data
    data, labels = load_dataset(args.d)

    # Train ML models
    print("MLP Training")
    mlp(data, labels, "mlp3.pkl")

    print("Knn Training")
    knn(data, labels, "knn3.pkl")



elif args.mode == "predict":
    from detection import *
    from convert import *


    # Load image
    img = cv2.imread(outputFile, 1)

    for j in range(len(x)):

        cropped=img[ y[j]:y[j]+h[j],x[j]:x[j]+w[j] ]

    cv2.imwrite('plaque immatriculation.jpg',cropped )
    # Apply image segmentation and extract digits
    digits = histogram_of_pixel_projection(cropped)

    # Load ML model
    clf = joblib.load(args.model)

    # List of predicted classes
    prediction = []

    for i in range(len(digits)):

        # Get digit
        digit = digits[i]
        # Make the image squared

        squared_digit = square(digit)

        # Resize the image
        resized_digit = cv2.resize(squared_digit, (28, 28), interpolation=cv2.INTER_AREA)

        # Convert to one dim vector
        one_vector_digit = np.array(resized_digit).ravel()

        # Predict digit class
        resultat = clf.predict([one_vector_digit])

        # Append to total predictions
        prediction.append(resultat[0])

    print(prediction)

else:
    print(" Error mode argument !")