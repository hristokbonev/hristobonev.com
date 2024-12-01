from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
import os
from dotenv import load_dotenv

load_dotenv()

recaptcha_secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
recaptcha_site_key = os.getenv("RECAPTCHA_SITE_KEY")


def create_assessment(
    token: str, recaptcha_action: str='submit', recaptcha_key: str=recaptcha_site_key, project_id: str = 'deep-lore-428512-u7'
) -> Assessment:
    """Create an assessment to analyze the risk of a UI action."""
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

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

    try:
        # Send the request and get the response
        response = client.create_assessment(request)

        # Check if the token is valid.
        if not response.token_properties.valid:
            print(
                "The CreateAssessment call failed because the token was "
                + "invalid for the following reasons: "
                + str(response.token_properties.invalid_reason)
            )
            return None  # Return None if token is invalid

        # Check if the expected action was executed.
        if response.token_properties.action != recaptcha_action:
            print(
                "The action attribute in your reCAPTCHA tag does"
                + " not match the action you are expecting to score"
            )
            return None  # Return None if action doesn't match

        # If no issues, return the response
        return response

    except Exception as e:
        print(f"Error creating assessment: {e}")
        return None  # Return None if any exception occurs



def allow_action(token: str, recaptcha_action: str='submit', recaptcha_key: str=recaptcha_site_key, project_id: str = 'deep-lore-428512-u7') -> bool:
    
    response = create_assessment(token=token, recaptcha_action=recaptcha_action, recaptcha_key=recaptcha_key, project_id=project_id)
    return response.risk_analysis.score > 0.5