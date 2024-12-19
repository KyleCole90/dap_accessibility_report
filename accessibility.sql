SELECT
  wp.id AS WikiPageId,
  wp.title AS WikiPageTitle,
  wp.body AS Body,
  c.id AS CourseId,
  u.name AS TeacherName
FROM
  wiki_pages wp
  JOIN courses c ON wp.context_id = c.id
  JOIN enrollments e ON c.id = e.course_id
  JOIN users u ON e.user_id = u.id
WHERE
  wp.workflow_state = 'active'
ORDER BY
  wp.id,
  c.id,
  u.name;