# Tennis-Ontology
This repository is the supplementary material of my master's thesis: "Ontology and Event Grammar Based Analysis of tennis", can be found at: http://web2py.iiit.ac.in/research_centres/publications/view_publication/mastersthesis/551

The code requires python and OpenCV Library.

	1. "annoatate.apk" is the android app to annotate a tennis match in real time based on the grammar of tennis.

	2. "score.py" computes the score based on annotations and "play.py" computes the information for statistics.

	3. "detection.py" Ball detection integrated with player detection. Displays bounding box over ball in motion and player in every frame.

	4. "trajectory_estimation.py" computes and stores the trajectory of the ball from which height of the trajectory, ball bounce coordinates can be computed. Also implemented curve fitting algorithm, which reduces the classification space to coefficients of equations.

	5. "tree.py" computes the probability of the next likely event. It computes it dynamically as the annotations are generated.

	6. "create_valid_data.py" is used to take user input and compute trajectories of valid/required shots only. It pauses at every event(abrupt change in the direction of the ball).

	7. "classifier.py" is used to classify the data created in step 6.

	8. "calibrate.m" is a matlab script which is used to calibrate the camera. This is an essential step in order to convert 2D coordinates to 3D.

	9. "convert_points.m" is a matlab script which converts 2D points to 3D based on the camera calibration in step 8. 
	 











