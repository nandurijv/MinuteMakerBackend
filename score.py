from rouge_score import rouge_scorer


scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

candidate_summary = "Action:1. Sarah to resolve the code conflict in the backend.2. Alex to coordinate with Sarah to ensure database queries align with the code rectification.3. Emily to adapt the UI to the resolved backend.4. Michael to develop a detailed test plan to cover all aspects affected by the error.5. Sarah to aim to fix the code conflict by the end of the day.6. Alex to expedite the process of aligning the database queries for a quicker resolution.7. Emily to have a revised UI reflecting the code rectification by the end of the day after tomorrow.8. Michael to commence testing once the code is revised and continue until all affected functionalities are thoroughly checked.Summary:In a team meeting, the lead developer discusses a recent error that has caused a setback in the project timeline. The error is identified as a code conflict in the backend, and the team members propose solutions to resolve it. They plan to rectify the code conflict, align the database queries, adapt the UI, and conduct thorough testing. The team aims to have the code conflict fixed by the end of the day, with database adjustments and UI adaptations to follow. Testing will commence once the code is revised, and the team is committed to meeting the project deadline."



reference_summary = "Action:Sarah was tasked with resolving the identified code conflict in the back end.Alex will coordinate with Sarah to sync database queries with correction.Emily is planning to work on adapting the user interface to show resolved backend.Michael will develop a full test plan covering everything which was affected by the errors within two days.All this will be targeted to be done by the end of the day.Follow up:Scheduled for the end of the testing phase to understand the progress.Summary:The meeting addressed a critical error that had tremendously affected the project timeline. The developer team gathered to discuss the issue, propose solutions, and strategize on how to recover and meet the project deadline."

scores = scorer.score(reference_summary, candidate_summary)
for key in scores:
    print(f'{key}: {scores[key]}')