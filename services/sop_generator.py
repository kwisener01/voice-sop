from openai import OpenAI
import logging
import json

logger = logging.getLogger(__name__)


class SOPGenerator:
    """Service for generating SOPs using GPT-4"""

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"

    def generate_sop(self, transcript, customer_info=None):
        """
        Generate a comprehensive SOP from a conversation transcript

        Args:
            transcript (str): The conversation transcript
            customer_info (dict): Optional customer information

        Returns:
            str: Formatted SOP content
        """
        try:
            logger.info('Generating SOP from transcript')

            # Build context
            context = self._build_context(customer_info)

            # Create the prompt
            system_prompt = self._get_system_prompt()
            user_prompt = self._build_user_prompt(transcript, context)

            # Call GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            sop_content = response.choices[0].message.content

            logger.info('Successfully generated SOP')
            return sop_content

        except Exception as e:
            logger.error(f'Failed to generate SOP: {str(e)}')
            raise Exception(f'SOP Generation Error: {str(e)}')

    def _get_system_prompt(self):
        """Get the system prompt for SOP generation"""
        return """You are an expert in creating professional Standard Operating Procedures (SOPs).

Your task is to analyze conversation transcripts and create comprehensive, well-structured SOPs that are:
- Clear and easy to follow
- Properly formatted with sections and subsections
- Include all necessary details from the conversation
- Professional and suitable for business documentation
- Include safety warnings and prerequisites where applicable
- Have clear success criteria and troubleshooting steps

Format the SOP using proper markdown with:
- Title (# heading)
- Overview/Purpose section
- Prerequisites/Requirements
- Step-by-step procedures (numbered)
- Quality standards/Expected outcomes
- Troubleshooting common issues
- Revision history (date and version)

Be thorough but concise. Focus on actionable steps."""

    def _build_context(self, customer_info):
        """Build context string from customer info"""
        if not customer_info:
            return ""

        context_parts = []

        if customer_info.get('name'):
            context_parts.append(f"Customer: {customer_info['name']}")

        if customer_info.get('company'):
            context_parts.append(f"Company: {customer_info['company']}")

        if customer_info.get('department'):
            context_parts.append(f"Department: {customer_info['department']}")

        return "\n".join(context_parts)

    def _build_user_prompt(self, transcript, context):
        """Build the user prompt"""
        prompt = "Please create a comprehensive SOP based on the following conversation:\n\n"

        if context:
            prompt += f"CONTEXT:\n{context}\n\n"

        prompt += f"CONVERSATION TRANSCRIPT:\n{transcript}\n\n"
        prompt += "Generate a professional SOP document in markdown format based on this conversation."

        return prompt

    def generate_sop_structured(self, data):
        """
        Generate SOP from structured data (not transcript)

        Args:
            data (dict): Structured data with SOP components
                - title: SOP title
                - purpose: Purpose/overview
                - steps: List of steps
                - prerequisites: Prerequisites
                - notes: Additional notes

        Returns:
            str: Formatted SOP content
        """
        try:
            logger.info(f'Generating SOP from structured data: {data.get("title")}')

            prompt = f"""Create a professional SOP document with the following information:

Title: {data.get('title')}
Purpose: {data.get('purpose')}

Prerequisites:
{self._format_list(data.get('prerequisites', []))}

Steps:
{self._format_steps(data.get('steps', []))}

Additional Notes:
{data.get('notes', 'None')}

Format this as a professional markdown SOP document with proper sections."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f'Failed to generate structured SOP: {str(e)}')
            raise Exception(f'SOP Generation Error: {str(e)}')

    def _format_list(self, items):
        """Format a list of items"""
        if not items:
            return "None"
        return "\n".join([f"- {item}" for item in items])

    def _format_steps(self, steps):
        """Format numbered steps"""
        if not steps:
            return "No steps provided"
        return "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    def refine_sop(self, sop_content, feedback):
        """
        Refine an existing SOP based on feedback

        Args:
            sop_content (str): Existing SOP content
            feedback (str): Feedback for refinement

        Returns:
            str: Refined SOP content
        """
        try:
            logger.info('Refining SOP based on feedback')

            prompt = f"""Here is an existing SOP document:

{sop_content}

Please refine this SOP based on the following feedback:
{feedback}

Maintain the professional format and structure while incorporating the feedback."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f'Failed to refine SOP: {str(e)}')
            raise Exception(f'SOP Refinement Error: {str(e)}')
