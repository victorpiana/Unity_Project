using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class InteractorBehavior : MonoBehaviour
{
    private Dictionary<string, GameObject> overlappingGrabbables = new Dictionary<string, GameObject>();
    private Dictionary<string, GameObject> overlappingTriggers = new Dictionary<string, GameObject>();
    private GameObject heldObject = null;

    private void OnTriggerEnter(Collider other)
    {
        GrabbableBehavior gb = other.GetComponentInParent<GrabbableBehavior>();
        if (gb)
        {
            overlappingGrabbables[gb.gameObject.name] = gb.gameObject;
        }

        TriggerBehavior tb = other.GetComponentInParent<TriggerBehavior>();
        if (tb)
        {
            overlappingTriggers[tb.gameObject.name] = tb.gameObject;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        GrabbableBehavior gb = other.GetComponentInParent<GrabbableBehavior>();
        if (gb)
        {
            overlappingGrabbables.Remove(gb.gameObject.name);
        }

        TriggerBehavior tb = other.GetComponentInParent<TriggerBehavior>();
        if (tb)
        {
            overlappingTriggers.Remove(tb.gameObject.name);
        }
    }

    private GameObject GetNearestGrabbable()
    {
        GameObject nearest = null;
        float minDistance = Mathf.Infinity;

        foreach (var kvp in overlappingGrabbables)
        {
            float distance = Vector3.Distance(transform.position, kvp.Value.transform.position);
            if (distance < minDistance)
            {
                minDistance = distance;
                nearest = kvp.Value;
            }
        }

        return nearest;
    }

    private GameObject GetNearestTrigger()
    {
        GameObject nearest = null;
        float minDistance = Mathf.Infinity;

        foreach (var kvp in overlappingTriggers)
        {
            float distance = Vector3.Distance(transform.position, kvp.Value.transform.position);
            if (distance < minDistance)
            {
                minDistance = distance;
                nearest = kvp.Value;
            }
        }

        return nearest;
    }

    public void OnGrabAction(InputAction.CallbackContext context)
    {
        GameObject nearest = GetNearestGrabbable();
        if (nearest)
        {
            var grabbable = nearest.GetComponent<GrabbableBehavior>();
            if (context.started)
            {
                grabbable.TryGrab(gameObject);
                heldObject = nearest;
            }
            else if (context.canceled)
            {
                grabbable.TryRelease(gameObject);
                heldObject = null;
            }
        }
    }

    public void OnTriggerAction(InputAction.CallbackContext context)
    {
        GameObject nearest = GetNearestTrigger();
        if (nearest && context.started)
        {
            nearest.GetComponent<TriggerBehavior>()?.Trigger();
        }
    }
}
