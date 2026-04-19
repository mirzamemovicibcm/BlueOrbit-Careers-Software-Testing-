class CareerRepository:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _one(row):
        return dict(row) if row is not None else None

    def list_opportunities(self):
        rows = self.connection.execute(
            """
            SELECT
                o.*,
                COUNT(a.id) AS application_count
            FROM opportunities AS o
            LEFT JOIN applications AS a
                ON a.opportunity_id = o.id
            WHERE o.is_active = 1
            GROUP BY o.id
            ORDER BY o.created_at DESC, o.id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_opportunity(self, opportunity_id):
        row = self.connection.execute(
            """
            SELECT
                o.*,
                COUNT(a.id) AS application_count
            FROM opportunities AS o
            LEFT JOIN applications AS a
                ON a.opportunity_id = o.id
            WHERE o.id = ?
            GROUP BY o.id
            """,
            (opportunity_id,),
        ).fetchone()
        return self._one(row)

    def create_opportunity(self, payload):
        cursor = self.connection.execute(
            """
            INSERT INTO opportunities
                (title, company, location, category, work_mode, salary_range, summary)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["title"],
                payload["company"],
                payload["location"],
                payload["category"],
                payload["work_mode"],
                payload["salary_range"],
                payload["summary"],
            ),
        )
        self.connection.commit()
        return self.get_opportunity(cursor.lastrowid)

    def create_application(self, payload):
        cursor = self.connection.execute(
            """
            INSERT INTO applications
                (opportunity_id, applicant_name, applicant_email, portfolio_url, motivation, status)
            VALUES
                (?, ?, ?, ?, ?, 'New')
            """,
            (
                payload["opportunity_id"],
                payload["applicant_name"],
                payload["applicant_email"],
                payload["portfolio_url"],
                payload["motivation"],
            ),
        )
        self.connection.commit()
        return self.get_application(cursor.lastrowid)

    def get_application(self, application_id):
        row = self.connection.execute(
            """
            SELECT
                a.*,
                o.title AS opportunity_title,
                o.company AS opportunity_company
            FROM applications AS a
            JOIN opportunities AS o
                ON o.id = a.opportunity_id
            WHERE a.id = ?
            """,
            (application_id,),
        ).fetchone()
        return self._one(row)

    def list_recent_applications(self, limit=6):
        rows = self.connection.execute(
            """
            SELECT
                a.*,
                o.title AS opportunity_title,
                o.company AS opportunity_company
            FROM applications AS a
            JOIN opportunities AS o
                ON o.id = a.opportunity_id
            ORDER BY a.created_at DESC, a.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def list_applications(self):
        rows = self.connection.execute(
            """
            SELECT
                a.*,
                o.title AS opportunity_title,
                o.company AS opportunity_company
            FROM applications AS a
            JOIN opportunities AS o
                ON o.id = a.opportunity_id
            ORDER BY a.created_at DESC, a.id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def count_applications(self):
        return self.connection.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
