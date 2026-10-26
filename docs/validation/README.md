# Local verification artifacts

These files record INIT-01 checks on Windows/Python 3.13.5. `checks.json` stores commands and exit
codes; text logs store actual stdout/stderr. The dependency freeze excludes the editable project
path and is evidence for this environment, not a promised portable lock.

The synthetic run, predictions, and metrics snapshot the 16-point manually constructed fixture.
They are software wiring examples, not NAB/hidden results. Runtime values are tiny-run observations,
not a general speed benchmark. Input hash corresponds to tests/fixtures/synthetic_stream.csv;
output timing makes prediction byte hashes run-specific.

New substantive verification should use unique task/run directories. Link counts can increase
as documentation grows; logs describe the actual time at which each command ran.
