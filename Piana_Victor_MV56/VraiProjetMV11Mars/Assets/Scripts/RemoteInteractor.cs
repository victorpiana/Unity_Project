using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class RemoteInteractor : MonoBehaviour
{
    public float maxDistance = 10f;
    public LineRenderer lineRenderer;
    public Material validMaterial;
    public Material invalidMaterial;

    private GameObject currentTarget;
    private bool isActive = false;

    void Start()
    {
        if (lineRenderer == null)
            lineRenderer = GetComponent<LineRenderer>();

        lineRenderer.positionCount = 2;
        lineRenderer.enabled = false; // invisible au départ
    }

    void FixedUpdate()
    {
        if (!isActive) return;

        RaycastHit hit;
        Vector3 origin = transform.position;
        Vector3 direction = transform.forward;

        lineRenderer.SetPosition(0, origin);

        if (Physics.Raycast(origin, direction, out hit, maxDistance))
        {
            lineRenderer.SetPosition(1, hit.point);

            if (hit.collider.GetComponentInParent<TriggerBehavior>())
            {
                currentTarget = hit.collider.gameObject;
                lineRenderer.material = validMaterial;
            }
            else
            {
                currentTarget = null;
                lineRenderer.material = invalidMaterial;
            }
        }
        else
        {
            currentTarget = null;
            lineRenderer.SetPosition(1, origin + direction * maxDistance);
            lineRenderer.material = invalidMaterial;
        }
    }

    public void OnRemoteAction(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            isActive = true;
            lineRenderer.enabled = true;
        }

        if (context.canceled)
        {
            if (currentTarget != null)
            {
                var trigger = currentTarget.GetComponentInParent<TriggerBehavior>();
                if (trigger != null)
                {
                    trigger.Trigger();
                }
            }

            isActive = false;
            lineRenderer.enabled = false;
        }
    }
}
