SELECT s.Id as SpectrumId, sub.Id as SubmissionId, sp.Value as name FROM adapcompounddb.File f 
left join adapcompounddb.Submission sub on sub.Id = f.SubmissionId
left join adapcompounddb.Spectrum s on s.FileId = f.Id 
left join adapcompounddb.SpectrumProperty sp on sp.SpectrumId = s.Id
where sub.ExternalId = "ST000548" and sp.Name = "Original Name" limit 10000000;