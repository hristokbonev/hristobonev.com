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
    """Create an assessment to analyse the risk of a UI action.
    Args:
        project_id: Your Google Cloud project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
    """

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

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    else:
        # Get the risk score and the reason(s).
        # For more information on interpreting the assessment, see:
        # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (ID). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response


def allow_action(token: str, recaptcha_action: str='submit', recaptcha_key: str=recaptcha_site_key, project_id: str = 'deep-lore-428512-u7') -> bool:
    
    response = create_assessment(token=token, recaptcha_action=recaptcha_action, recaptcha_key=recaptcha_key, project_id=project_id)
    return response.risk_analysis.score > 0.5