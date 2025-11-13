using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;




public class InputsBehavior : MonoBehaviour
{
    // MAIN DROITE
    public Animator RightController;
    public GameObject rightThumbstick;
    public Animator rightHandAnimator;
    
    public InteractorBehavior rightInteractor;
    public InteractorBehavior leftInteractor;
    public RemoteInteractor rightRemoteInteractor;


    // MAIN GAUCHE
    public Animator LeftController;
    public GameObject leftThumbstick;
    public Animator leftHandAnimator;

    public void OnAPressed(InputAction.CallbackContext context)
    { 
        if (context.started)
        {
            Debug.Log("A Pressed");
            if (RightController)
            {
                RightController.SetBool("APressed", true);
            }
        }
        if (context.canceled)
        {
            Debug.Log("A Released");
            if (RightController)
            {
                RightController.SetBool("APressed", false);
            }
        }
    }

    public void OnBPressed(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            Debug.Log("B Pressed");
            if (RightController)
            {
                RightController.SetBool("BPressed", true);
            }
        }
        if (context.canceled)
        {
            Debug.Log("B Released");
            if (RightController)
            {
                RightController.SetBool("BPressed", false);
            }
        }
    }

    public void OnTriggerAxis(InputAction.CallbackContext context)
    {
        if(RightController)
        {
            RightController.SetFloat("RightTrigger", context.ReadValue<float>());
        }
    }

    public void OnThumbstickAxis(InputAction.CallbackContext context)
    {
        if (rightThumbstick)
        {
            Vector2 thumbstickValue = context.ReadValue<Vector2>();
            rightThumbstick.transform.localEulerAngles = new Vector3(thumbstickValue.y, 0, -
           thumbstickValue.x) * 15f;
        }
    }

    public void OnGripAxis(InputAction.CallbackContext context)
    {
        if (rightHandAnimator)
        {
            rightHandAnimator.SetFloat("Close", context.ReadValue<float>());
        }
    }
    public void OnTriggerTouch(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            if (rightHandAnimator)
            {
                rightHandAnimator.SetBool("Point", false);
            }
        }
        if (context.canceled)
        {
            if (rightHandAnimator)
            {
                rightHandAnimator.SetBool("Point", true);
            }
        }
    }




    // MAIN GAUCHE 

    public void OnXPressed(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            Debug.Log("X Pressed");
            if (LeftController != null)
            {
                LeftController.SetBool("XPressed", true);
            }
        }
        if (context.canceled)
        {
            Debug.Log("X Released");
            if (LeftController != null)
            {
                LeftController.SetBool("XPressed", false);
            }
        }
    }

    public void OnYPressed(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            Debug.Log("Y Pressed");
            if (LeftController != null)
            {
                LeftController.SetBool("YPressed", true);
            }
        }
        if (context.canceled)
        {
            Debug.Log("Y Released");
            if (LeftController != null)
            {
                LeftController.SetBool("YPressed", false);
            }
        }
    }

    public void OnLeftTriggerAxis(InputAction.CallbackContext context)
    {
        if (LeftController != null)
        {
            LeftController.SetFloat("LeftTrigger", context.ReadValue<float>());
        }
    }

    public void OnLeftThumbstickAxis(InputAction.CallbackContext context)
    {
        Debug.Log("Left Thumbstick Moved");
        if (leftThumbstick)
        {
            Vector2 thumbstickValue = context.ReadValue<Vector2>();
            leftThumbstick.transform.localEulerAngles = new Vector3(thumbstickValue.y, 0, -thumbstickValue.x) * 15f;
        }
    }

    public void OnLeftGripAxis(InputAction.CallbackContext context)
    {
        if (leftHandAnimator != null)
        {
            leftHandAnimator.SetFloat("Close", context.ReadValue<float>());
        }
    }

    public void OnLeftTriggerTouch(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            if (leftHandAnimator != null)
            {
                leftHandAnimator.SetBool("Point", false);
            }
        }
        if (context.canceled)
        {
            if (leftHandAnimator != null)
            {
                leftHandAnimator.SetBool("Point", true);
            }
        }
    }

    public void OnRightTriggerButton(InputAction.CallbackContext context)
    {
        if (rightInteractor)
        {
            rightInteractor.OnTriggerAction(context);
        }
    }
    public void OnLeftTriggerButton(InputAction.CallbackContext context)
    {
        if (leftInteractor)
        {
            leftInteractor.OnTriggerAction(context);
        }
    }

    public void OnAExtended(InputAction.CallbackContext context)
    {
        if (rightRemoteInteractor)
        {
            rightRemoteInteractor.OnRemoteAction(context);
        }
    }


}