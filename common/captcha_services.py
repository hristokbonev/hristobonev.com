from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
import os
from dotenv import load_dotenv

load_dotenv()

recaptcha_secret_key = os.getenv("RECAPTCHA_SECRET_KEY")

def create_assessment(
    token: str, project_id: str = 'deep-lore-428512-u7', recaptcha_key: str = recaptcha_secret_key, recaptcha_action: str = 'submit'
) -> Assessment:
    """Create an assessment to analyse the risk of a UI action.
    Args:
        project_id: Your Google Cloud project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        
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

def allow_action(token: str, project_id: str = 'deep-lore-428512-u7', recaptcha_key: str = recaptcha_secret_key, recaptcha_action: str = 'submit') -> bool:
    """Create an assessment and allow the action if the risk is low.
    Args:
        project_id: Your Google Cloud project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
    """   
    response = create_assessment(token, project_id, recaptcha_key, recaptcha_action)
    return response.risk_analysis.score > 0.5