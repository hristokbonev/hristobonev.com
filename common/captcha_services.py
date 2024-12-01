from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
import os
from dotenv import load_dotenv

load_dotenv()

recaptcha_secret_key = os.getenv("RECAPTCHA_SECRET_KEY")

def create_assessment_and_allow_action(
        recaptcha_key: str, token: str, recaptcha_action: str = 'submit', score_threshold: float = 0.5, project_id: str = 'deep-lore-428512-u7'
) -> bool:
    """Create an assessment and allow action if the reCAPTCHA score passes the threshold.
    Args:
        project_id: Your Google Cloud project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app.
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
        score_threshold: The score threshold above which the action is allowed.
    Returns:
        True if the action is allowed, False otherwise.
    """
    
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    recaptcha_key = recaptcha_secret_key

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return False

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return False

    # Check the reCAPTCHA risk score and allow action if it passes the threshold.
    score = response.risk_analysis.score
    if score >= score_threshold:
        print(f"Action allowed. reCAPTCHA score: {score}")
        return True
    else:
        print(f"Action not allowed. reCAPTCHA score: {score}")
        return False
