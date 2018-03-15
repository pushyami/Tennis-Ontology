# Tennis-Ontology
This repository is the supplementary material of my master's thesis: "Ontology and Event Grammar Based Analysis of tennis", can be found at: http://web2py.iiit.ac.in/research_centres/publications/view_publication/mastersthesis/551

The code requires python and OpenCV Library.
	1. "annoatate.apk" is the android app to annotate a tennis match in real time based on the grammar of tennis.
	2. "score.py" computes the score based on annotations.
	3. "detection.py" Ball detection integrated with player detection. Displays bounding box over ball in motion and player in every frame.
	4. "trajectory_estimation.py" computes and stores the trajectory of the ball from which height of the trajectory, ball bounce coordinates can be computed. Also implemented curve fitting algorithm, which reduces the classification space to coefficients of equations.
	 











