-- Update the user's average_score in the users table
-- Compute the weighted average score
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE weighted_avg_score FLOAT;

    SELECT SUM(c.score * p.weight) / SUM(p.weight)
    INTO weighted_avg_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;

    UPDATE users
    SET average_score = IFNULL(weighted_avg_score, 0)
    WHERE id = p_user_id;
END //

DELIMITER ;
