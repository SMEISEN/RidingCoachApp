from backend.database import db
from sqlalchemy.orm import column_property
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from functools import wraps


# workaround https://github.com/tiangolo/pydantic-sqlalchemy/issues/10
def custom_column_property(func):
    @wraps(func)
    def wrapper(*args, default=None, nullable=True, **kwargs):
        v = func(*args, **kwargs)
        for column in v.columns:
            column.default = default
            column.nullable = nullable
        return v

    return wrapper


db.column_property = custom_column_property(column_property)


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


db.utcnow = UtcNow()
