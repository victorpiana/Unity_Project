using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class TriggerBehavior : MonoBehaviour
{
    public UnityEvent OnTriggered;

    public void Trigger()
    {
        OnTriggered?.Invoke();
    }
}
