import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text


db_connection_string=os.environ['DB_CONNECTION_STRING_JOVIAN_CAREERS_WEBSITE']

engine = create_engine(db_connection_string,
          connect_args={
                  "ssl": {
                      "ssl_ca": "/etc/ssl/cert.pem"
                  }
              })



def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs=[]
    for row in result.all():
      jobs.append(row._asdict())
    return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
    SelectStatement="SELECT * FROM jobs WHERE id=" + id
    result=conn.execute(
      text(SelectStatement)
    )
    rows=result.all()
    if len(rows)==0:
      return None
    else:
      return rows[0]._asdict()
    

def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    row={
      "job_id": job_id,
      "full_name": data["full_name"],
      "email": data["email"],
      "linkin_url": data["linkin_url"],
      "education": data["education"],
      "work_experience": data["work_experience"],
      "resume_url": data["resume_url"]
    }
    queryString=text("INSERT INTO applications (job_id, full_name, email, linkin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkin_url, :education, :work_experience, :resume_url)"
    )
  
    conn.execute(queryString, row)
    