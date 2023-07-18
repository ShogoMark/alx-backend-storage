-- A stored procedure that computes and store the avg score for a student

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER !!
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE total_score INT DEFAULT 0;
	DECLARE project_count INT DEFAULT 0;

	-- Compute the score
	SELECT SUM(score) INTO total_score
	FROM corrections
	WHERE corrections.user_id = user_id;

	-- Compute the project counts
	SELECT COUNT(*) INTO project_count
	FROM corrections
	WHERE corrections.user_id = user_id;

	-- update the avg score in the user table
	UPDATE users
	SET users.average_score = IF(
		project_count = 0,
		0,
		total_score / project_count
	)
	WHERE id = user_id;
END!!
DELIMITER ;
